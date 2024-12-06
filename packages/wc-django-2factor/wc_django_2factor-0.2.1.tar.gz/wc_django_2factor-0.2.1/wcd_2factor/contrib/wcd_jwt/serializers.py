from django.utils.translation import pgettext
from django.contrib.auth import logout
from rest_framework.exceptions import ValidationError
from wcd_jwt.serializers import TokenObtainPairSerializer

from wcd_2factor.confirmer import default_confirmer
from wcd_2factor.contrib.drf.fields import PrimaryKeyRelatedField
from wcd_2factor.contrib.drf.serializers import UserConfigExternalDisplaySerializer
from wcd_2factor.models import ConfirmationState


class TwoFactorTokenObtainPairSerializer(TokenObtainPairSerializer):
    confirmer = default_confirmer
    confirmation_id = PrimaryKeyRelatedField(
        queryset=lambda self: (
            ConfirmationState.objects
            .filter(status=ConfirmationState.Status.CONFIRMED)
        ),
        required=False,
    )

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        configs = [
            x for x in self.confirmer.get_user_configs(user=user)
            if x.is_available()
        ]
        data['authenticated'] = True

        if len(configs) == 0:
            return data

        confirmation_id = attrs.get('confirmation_id')

        if confirmation_id is None:
            logout(self.context.get('request'))

            data['authenticated'] = False
            data['configs'] = configs

            return data

        available, confirmation = self.confirmer.check(
            id=confirmation_id, context=self.context,
        )

        if not available or confirmation.user_config_id not in [
            x.pk for x in configs
        ]:
            raise ValidationError({
                'confirmation_id': pgettext('wcd_2factor', 'Wrong confirmation.'),
            })

        self.confirmer.use(confirmation=confirmation, context=self.context)

        return data

    def commit(self):
        v = self.validated_data
        authenticated = v.get('authenticated', False)

        if authenticated:
            return {
                'authenticated': authenticated,
                'refresh': str(v['refresh']),
                'access': str(v['access']),
            }

        return {
            'authenticated': authenticated,
            'configs': UserConfigExternalDisplaySerializer(v['configs'], many=True).data,
        }
