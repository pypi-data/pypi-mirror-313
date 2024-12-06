from typing import *
from uuid import uuid4
from django.db import models
from django.utils.translation import pgettext_lazy, pgettext
from wcd_notifications.compat import TextChoices

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

from django.conf import settings
from django.utils.translation import pgettext_lazy
from django.db import models

from ..utils import get_json_encoder
from .base import Timestamped
from .method_configs import MethodConfig
from .user_configs import UserConfig


__all__ = 'ConfirmationState',


class ConfirmationStatus(TextChoices):
    NEW = '015-new', pgettext_lazy('wcd_2factor:const', 'New')
    IN_PROCESS = '025-in_process', pgettext_lazy('wcd_2factor:const', 'In process')
    CONFIRMED = '085-confirmed', pgettext_lazy('wcd_2factor:const', 'Confirmed')


class ConfirmationState(Timestamped):
    Status = ConfirmationStatus

    class Meta:
        verbose_name = pgettext_lazy('wcd_2factor:models', 'Confirmation state')
        verbose_name_plural = pgettext_lazy(
            'wcd_2factor:models', 'Confirmation states'
        )

    id = models.UUIDField(
        primary_key=True, verbose_name=pgettext_lazy('wcd_2factor:models', 'ID'),
        default=uuid4,
    )
    method_config = models.ForeignKey(
        to=MethodConfig, on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('wcd_2factor:models', 'Method'),
        related_name='wcd_2factor_confirmation_states', blank=False, null=True,
    )
    user_config = models.ForeignKey(
        to=UserConfig, on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('wcd_2factor:models', 'User connection'),
        related_name='wcd_2factor_confirmation_states', blank=True, null=True,
    )
    status = models.CharField(
        verbose_name=pgettext_lazy('wcd_2factor:models', 'Status'),
        max_length=32, choices=Status.choices, default=Status.NEW,
    )
    state = JSONField(
        verbose_name=pgettext_lazy('wcd_2factor:models', 'Config'),
        encoder=get_json_encoder(), default=dict, blank=True, null=False,
    )

    def __str__(self):
        return (
            pgettext(
                'wcd_2factor:models',
                '#{method} confirmation: {status}.',
            )
            .format(
                method=self.method_config_id,
                status=self.get_status_display(),
            )
        )

    def is_available(self):
        return (
            self.status == self.Status.CONFIRMED
            and
            (
                self.user_config_id is None
                or
                (
                    self.user_config.is_active
                    and
                    self.user_config.status == self.user_config.Status.CONFIRMED
                )
            )
            and
            self.method_config.is_active
        )
