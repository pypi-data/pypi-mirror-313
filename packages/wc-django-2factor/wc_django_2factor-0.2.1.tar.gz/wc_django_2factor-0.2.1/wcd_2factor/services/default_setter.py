from typing import *
from django.db import models
from wcd_2factor.models import MethodConfig, UserConfig


__all__ = 'set_method', 'set_user',


def set_method(
    *,
    method_config: Optional[MethodConfig] = None,
    id: Optional[int] = None,
):
    assert id is not None or method_config is not None, (
        'Either `id` or `method_config` must not be None.'
    )

    if id is None:
        id = method_config.pk

    return (
        MethodConfig.objects.all()
        .annotate(_is=models.F('pk') == id)
        .update(is_default=models.F('_is'))
    )


def set_user(
    *,
    user_config: Optional[UserConfig] = None,
    id: Optional[int] = None,
    user_id: Optional[int] = None,
):
    assert (id is not None and user_id is not None) or user_config is not None, (
        'Either both `id` and `user_id` or `user_config` must not be None.'
    )

    if id is None:
        id = user_config.pk

    if user_id is None:
        user_id = user_config.user_id

    return (
        UserConfig.objects
        .filter(user_id=user_id)
        .annotate(_is=models.F('pk') == id)
        .update(is_default=models.F('_is'))
    )