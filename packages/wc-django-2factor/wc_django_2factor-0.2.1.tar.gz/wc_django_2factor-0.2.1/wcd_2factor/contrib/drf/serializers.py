from typing import *
from rest_framework import serializers
from django.conf import settings as dj_settings
from django.db import transaction
from django.utils.translation import pgettext_lazy

from wcd_2factor.models import MethodConfig, UserConfig, ConfirmationState
from wcd_2factor.confirmer import default_confirmer
from wcd_2factor.exceptions import TwoFactorError
from wcd_2factor.services import default_setter

from .helpers import handle_pydantic_validation
from .fields import PrimaryKeyRelatedField


T = TypeVar('T')


class Serializer(serializers.Serializer):
    def fail_non_field(self, key, **kwargs):
        try:
            self.fail(key, **kwargs)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'non_field_errors': e.detail})


class ConfirmationStateDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationState
        fields = 'id', 'status', 'is_available'


class MethodConfigDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodConfig
        fields = 'id', 'title', 'method', 'is_default',
        read_only_fields = fields

    def get_title(self, obj: MethodConfig):
        return obj.get_title()


class UserConfigDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfig
        fields = (
            'id', 'title', 'status', 'method_config_id', 'method_config',
            'config',
            'is_active', 'is_default', 'is_available',
        )
        read_only_fields = fields

    method_config = MethodConfigDisplaySerializer()

    def get_title(self, obj: UserConfig):
        return obj.get_title()


class UserConfigExternalDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfig
        fields = (
            'id', 'title', 'status', 'method_config_id', 'method_config',
            'is_active', 'is_default', 'is_available',
        )
        read_only_fields = fields

    method_config = MethodConfigDisplaySerializer()

    def get_title(self, obj: UserConfig):
        return obj.get_title()


class ErrorHandlerMixin(Serializer):
    default_error_messages = {
        'unknown_error': pgettext_lazy('wcd_2factor:errors', 'Unknown error.'),
    }

    def handle_errors(self, callback: Callable[[], T], pydantic_errors_path: Sequence[str] = ['non_field_errors']) -> T:
        try:
            with handle_pydantic_validation(pydantic_errors_path) as handler:
                return callback()
            handler.reraise()
        except TwoFactorError as e:
            raise serializers.ValidationError({'non_field_errors': [str(e)]})
        except AssertionError as e:
            if dj_settings.DEBUG:
                raise serializers.ValidationError({'non_field_errors': ['DEBUG: ' + str(e)]})

        self.fail_non_field('unknown_error')


class UserConfigCreateSerializer(ErrorHandlerMixin, serializers.ModelSerializer):
    confirmer = default_confirmer

    class Meta:
        model = UserConfig
        fields = (
            'id', 'title', 'status', 'method_config_id',
            'config',
            'is_active', 'is_default',
        )
        read_only_fields = 'id', 'status', 'is_available',
        extra_kwargs = {
            field: {'required': True}
            for field in (
                'method_config_id', 'config', 'is_active', 'is_default',
            )
        }

    method_config_id = PrimaryKeyRelatedField(
        queryset=lambda self: self.parent.confirmer.get_method_configs(),
    )

    def inject_method_config(self, attrs):
        attrs['method_config'] = attrs.pop('method_config_id')

        return attrs

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs = self.inject_method_config(attrs)
        attrs['user'] = self.context.get('user') or self.context['request'].user

        with handle_pydantic_validation(['config']) as handled:
            self.confirmer.make_user_config_dto(
                descriptor=self.confirmer.get_descriptor(attrs['method_config'].method),
                raw=attrs['config'], should_raise=True,
            )
        handled.reraise()

        return attrs

    def save(self, **kwargs):
        method = super().save
        return self.handle_errors(lambda: method(**kwargs))

    def create(self, validated_data):
        config = validated_data.pop('config')
        instance = super().create(validated_data)

        make_confirmation = self.confirmer.change_user_config(
            instance, new=config,
            method_config=validated_data['method_config'],
            context={**self.context, 'serializer': self},
        )
        instance.status = (
            UserConfig.Status.CONFIRMED
            if make_confirmation is None else
            UserConfig.Status.IN_PROCESS
        )
        instance.save(update_fields=['config', 'status'])

        if instance.is_default:
            default_setter.set_user(user_config=instance)

        self.confirmation = make_confirmation() if make_confirmation is not None else None

        return instance


class UserConfigUpdateSerializer(UserConfigCreateSerializer):
    class Meta(UserConfigCreateSerializer.Meta):
        read_only_fields = 'id', 'status', 'is_available', 'method_config_id',

    method_config_id = None

    def inject_method_config(self, attrs):
        attrs['method_config'] = self.instance.method_config

        return attrs

    def update(self, instance, validated_data):
        config = validated_data.pop('config')
        instance = super().update(instance, validated_data)

        make_confirmation = self.confirmer.change_user_config(
            instance, new=config,
            method_config=validated_data['method_config'],
            context={**self.context, 'serializer': self},
        )

        if make_confirmation is not None:
            instance.status = UserConfig.Status.IN_PROCESS

        instance.save(update_fields=['config', 'status'])

        if instance.is_default:
            default_setter.set_user(user_config=instance)

        self.confirmation = make_confirmation() if make_confirmation is not None else None

        return instance


class UserConfigConfirmSerializer(ErrorHandlerMixin, serializers.Serializer):
    default_error_messages = {
        'wrong_config': pgettext_lazy(
            'wcd_2factor:errors',
            'User config can not be confirmed with this confirmation.',
        ),
        'failed_to_confirm': pgettext_lazy(
            'wcd_2factor:errors',
            'Failed to confirm.',
        ),
    }
    confirmer = default_confirmer
    id = PrimaryKeyRelatedField(
        write_only=True, required=True,
        queryset=lambda self: (
            self.parent.confirmer
            .get_user_configs(
                user=(
                    self.parent.context.get('user')
                    or
                    self.parent.context.get('request').user
                )
            )
            .filter(method_config__is_active=True)
            .exclude(status=UserConfig.Status.CONFIRMED)
        )
    )
    confirmation_id = PrimaryKeyRelatedField(
        queryset=lambda self: ConfirmationState.objects.exclude(status=ConfirmationState.Status.CONFIRMED),
        write_only=True,
    )
    data = serializers.DictField(required=True, write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['confirmation_id'].user_config_id is None:
            attrs['confirmation_id'].user_config = attrs['id']

        if attrs['id'].pk != attrs['confirmation_id'].user_config_id:
            self.fail('wrong_config')

        return attrs

    @transaction.atomic
    def commit(self):
        confirmation = self.handle_errors(lambda: self.confirmer.confirm(
            confirmation=self.validated_data['confirmation_id'],
            data=self.validated_data['data'],
            context=self.context,
        ), pydantic_errors_path=['data'])

        config: UserConfig = confirmation.user_config
        config.status = UserConfig.Status.CONFIRMED

        if (
            confirmation.status != ConfirmationState.Status.CONFIRMED
            or
            not config.method_config.is_available()
        ):
            self.fail_non_field('failed_to_confirm')

        self.confirmer.use(confirmation=confirmation)
        config.save(update_fields=['status'])

        return config


class ConfirmationRequestSerializer(ErrorHandlerMixin, serializers.Serializer):
    default_error_messages = {
        'empty_config': pgettext_lazy(
            'wcd_2factor:errors',
            'Either method_config_id or user_config_id is required.',
        ),
    }
    confirmer = default_confirmer
    method_config_id = PrimaryKeyRelatedField(
        queryset=lambda self: self.parent.confirmer.get_method_configs(),
        write_only=True, required=False,
    )
    user_config_id = PrimaryKeyRelatedField(
        write_only=True, required=False,
        queryset=lambda self: (
            self.parent.confirmer.get_user_configs(
                user=(
                    self.parent.context.get('user')
                    or
                    self.parent.context.get('request').user
                )
            )
        )
    )
    data = serializers.DictField(required=True, write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if not attrs.get('method_config_id') and not attrs.get('user_config_id'):
            self.fail('empty_config')

        return attrs

    def commit(self):
        return self.handle_errors(lambda: self.confirmer.request_confirmation(
            method_config=self.validated_data.get('method_config_id'),
            user_config=self.validated_data.get('user_config_id'),
            state=self.validated_data['data'],
            context=self.context,
        ), pydantic_errors_path=['data'])


class ConfirmSerializer(ErrorHandlerMixin, serializers.Serializer):
    default_error_messages = {
        'wrong_config': pgettext_lazy(
            'wcd_2factor:errors',
            'Can not be confirmed with unavailable config.',
        ),
        'failed_to_confirm': pgettext_lazy(
            'wcd_2factor:errors',
            'Failed to confirm.',
        ),
    }
    confirmer = default_confirmer
    id = PrimaryKeyRelatedField(
        queryset=lambda self: ConfirmationState.objects.exclude(status=ConfirmationState.Status.CONFIRMED),
        write_only=True,
    )
    data = serializers.DictField(required=True, write_only=True)

    def validate_id(self, value):
        if not value.method_config.is_available():
            self.fail('wrong_config')

        if value.user_config_id is not None and not value.user_config.is_available():
            self.fail('wrong_config')

        return value

    def commit(self):
        confirmation = self.handle_errors(lambda: self.confirmer.confirm(
            confirmation=self.validated_data['id'],
            data=self.validated_data['data'],
            context=self.context,
        ), pydantic_errors_path=['data'])

        if not confirmation.is_available():
            self.fail_non_field('failed_to_confirm')

        return confirmation
