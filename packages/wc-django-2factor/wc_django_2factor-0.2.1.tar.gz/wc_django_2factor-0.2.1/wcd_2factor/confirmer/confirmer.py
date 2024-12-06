from typing import *
from uuid import UUID, uuid4
from pydantic import ValidationError

from django.db import models
from django.utils.translation import pgettext_lazy

from wcd_2factor.models import MethodConfig, UserConfig, ConfirmationState
from wcd_2factor.registries import (
    DTO, Registry, method_config_registry, MethodConfigDescriptor,
)
from wcd_2factor.exceptions import ConfirmationFailed, MethodMissing

from .backends import Backend


__all__ = 'Confirmer', 'default_confirmer',

D = TypeVar('D', bound=DTO)


class Confirmer:
    registry: Registry = method_config_registry

    def __init__(self, registry: Optional[Registry] = None):
        self.registry = registry if registry is not None else self.registry

        assert self.registry is not None, (
            'Registry must be specified on a Confirmer or passed on init.'
        )

    def get_methods(self) -> Tuple[str]:
        return tuple(self.registry.keys())

    def get_method_configs(self):
        return MethodConfig.objects.active().filter(method__in=self.get_methods())

    def get_user_configs(
        self,
        user: Optional[models.Model] = None,
        user_id: Optional[Any] = None,
    ):
        assert user is not None or user_id is not None, (
            'Either `user` or `user_id` must not be None.'
        )
        if user_id is None:
            user_id = user.pk

        return UserConfig.objects.filter(
            user_id=user_id,
            method_config__method__in=self.get_methods(),
            method_config__is_active=True,
        )

    def get_descriptor(self, method: str) -> Optional[MethodConfigDescriptor]:
        return self.registry.get(method)

    def _make_dto(
        self,
        raw: dict,
        dto_class: Optional[Type[D]],
        should_raise: bool = False,
    ) -> Optional[D]:
        if dto_class is None:
            return None

        try:
            return dto_class.model_validate(raw)
        except ValidationError as e:
            if should_raise:
                raise e

            return None

    def make_method_config_dto(
        self,
        descriptor: Optional[MethodConfigDescriptor] = None,
        method_config: Optional[MethodConfig] = None,
        raw: Optional[dict] = None,
        should_raise: bool = False,
    ):
        assert method_config is None or raw is None, (
            'Either `method_config` or `raw` must not be specified.'
        )
        if method_config is None and raw is None:
            return None

        return self._make_dto(
            raw if raw is not None else method_config.config,
            descriptor.config_global_dto,
            should_raise=should_raise,
        )

    def make_user_config_dto(
        self,
        descriptor: Optional[MethodConfigDescriptor] = None,
        user_config: Optional[UserConfig] = None,
        raw: Optional[dict] = None,
        should_raise: bool = False,
    ):
        assert user_config is None or raw is None, (
            'Either `user_config` or `raw` must not be specified.'
        )

        if user_config is None and raw is None:
            return None

        return self._make_dto(
            raw if raw is not None else user_config.config,
            descriptor.config_user_dto,
            should_raise=should_raise,
        )

    def _normalize_configs(
        self,
        method_config: Optional[MethodConfig],
        user_config: Optional[UserConfig],
    ) -> Tuple[MethodConfig, Optional[UserConfig]]:
        assert method_config is not None or user_config is not None, (
            'Either `method` or `user_config` must not be None.'
        )

        if user_config is not None and method_config is None:
            method_config = user_config.method_config

        assert user_config is None or method_config.pk == user_config.method_config_id, (
            'User config must have the same method as the provided method config.'
        )

        if user_config is not None:
            user_config.method_config = method_config

        return method_config, user_config

    def make_backend(
        self,
        *,
        method_config: Optional[MethodConfig] = None,
        user_config: Optional[UserConfig] = None,
        context: Optional[dict] = None,
        should_raise: bool = False,
    ) -> Optional[Backend]:
        method_config, user_config = self._normalize_configs(
            method_config, user_config,
        )

        descriptor = self.get_descriptor(method_config.method)

        if descriptor is None:
            if should_raise:
                raise MethodMissing(method=method_config.method)

            return None

        method_dto = self.make_method_config_dto(descriptor, method_config)

        if method_dto is None:
            if should_raise:
                raise MethodMissing(method=method_config.method)

            return None

        context = {
            **(context if context is not None else {}),
            'method_config_instance': method_config,
            'user_config_instance': user_config,
            'confirmer': self,
            'descriptor': descriptor,
        }

        backend = descriptor.backend_class(
            method_config=method_dto,
            user_config=self.make_user_config_dto(descriptor, user_config),
            confirmer=self,
            context=context,
        )

        return backend

    def change_user_config(
        self,
        user_config: UserConfig,
        new: Union[D, dict],
        *,
        backend: Optional[Backend] = None,
        method_config: Optional[MethodConfig] = None,
        context: Optional[dict] = None,
    ) -> Optional[Callable[[], ConfirmationState]]:
        method_config, user_config = self._normalize_configs(
            method_config, user_config,
        )
        user_config.method_config = method_config

        if backend is None:
            backend = self.make_backend(
                method_config=method_config, user_config=user_config,
                context=context, should_raise=True,
            )

        if isinstance(new, dict):
            new = self.make_user_config_dto(
                descriptor=self.get_descriptor(method_config.method),
                raw=new, should_raise=True,
            )

        should_confirm, state = backend.change_user_config(
            new, context=context,
        )
        user_config.config = new.model_dump()

        if not should_confirm:
            return None

        state = state if state is not None else {}

        return lambda: self.request_confirmation(
            method_config=method_config, user_config=user_config,
            state=state, backend=backend, context=context,
        )

    def request_confirmation(
        self,
        *,
        method_config: Optional[MethodConfig] = None,
        user_config: Optional[UserConfig] = None,
        backend: Optional[Backend] = None,
        state: Optional[dict] = None,
        context: Optional[dict] = None,
    ):
        method_config, user_config = self._normalize_configs(
            method_config, user_config,
        )

        if backend is None:
            backend = self.make_backend(
                method_config=method_config, user_config=user_config,
                context=context, should_raise=True,
            )

        id = uuid4()
        context = {**(context if context is not None else {}), 'confirmation_id': id}
        status, state = backend.request_confirmation(
            state if state is not None else {}, context=context,
        )

        return ConfirmationState.objects.create(
            id=id, method_config=method_config, user_config=user_config,
            status=status, state=state,
        )

    def _resolve_confirmation(
        self,
        queryset: models.QuerySet,
        *,
        id: Optional[UUID] = None,
        confirmation: Optional[ConfirmationState] = None,
    ) -> Optional[ConfirmationState]:
        assert id is not None or confirmation is not None, (
            'Either `id` or `confirmation` must not be None.'
        )

        if confirmation is None:
            confirmation = (
                queryset
                .filter(id=id)
                .select_related('user_config', 'method_config')
                .first()
            )

        return confirmation

    def confirm(
        self,
        *,
        id: Optional[UUID] = None,
        confirmation: Optional[ConfirmationState] = None,
        data: Optional[dict] = None,
        backend: Optional[Backend] = None,
        context: Optional[dict] = None,
    ) -> ConfirmationState:
        confirmation = self._resolve_confirmation(
            ConfirmationState.objects.exclude(status=ConfirmationState.Status.CONFIRMED),
            id=id, confirmation=confirmation,
        )

        if confirmation is None:
            raise ConfirmationFailed(pgettext_lazy(
                'wcd_2factor:exception',
                'No unconfirmed confirmation found.',
            ))

        if backend is None:
            backend = self.make_backend(
                method_config=confirmation.method_config,
                user_config=confirmation.user_config,
                context=context, should_raise=True,
            )

        success = backend.confirm(
            state=confirmation.state, user_data=data, context=context,
        )

        if success:
            confirmation.status = ConfirmationState.Status.CONFIRMED
            confirmation.save(update_fields=('status',))

        return confirmation

    def check(
        self,
        *,
        id: Optional[UUID] = None,
        confirmation: Optional[ConfirmationState] = None,
        context: Optional[dict] = None,
    ) -> Tuple[bool, Optional[ConfirmationState]]:
        confirmation = self._resolve_confirmation(
            ConfirmationState.objects.all(),
            id=id, confirmation=confirmation,
        )

        if confirmation is None:
            return False, None

        return confirmation.is_available(), confirmation

    def use(
        self,
        *,
        id: Optional[UUID] = None,
        confirmation: Optional[ConfirmationState] = None,
        context: Optional[dict] = None,
    ) -> Tuple[bool, Optional[ConfirmationState]]:
        available, confirmation = self.check(id=id, confirmation=confirmation)

        if not available:
            return False, confirmation

        confirmation.delete()

        return True, confirmation


default_confirmer = Confirmer()
