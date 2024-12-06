from typing import *
from django.db import models
from django.conf import settings as dj_settings
from django.utils.translation import pgettext_lazy, pgettext
from wcd_notifications.compat import TextChoices

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

from django.utils.translation import pgettext_lazy
from django.db import models

from ..utils import get_json_encoder
from .base import Timestamped
from .method_configs import MethodConfig


__all__ = 'UserConfig',


class UserConfigStatus(TextChoices):
    NEW = '015-new', pgettext_lazy('wcd_2factor:const', 'New')
    IN_PROCESS = '025-in_process', pgettext_lazy('wcd_2factor:const', 'In process')
    CONFIRMED = '085-confirmed', pgettext_lazy('wcd_2factor:const', 'Confirmed')


class UserConfigQuerySet(models.QuerySet):
    model: Type['UserConfig']

    def active(self):
        return self.filter(
            is_active=True,
            method_config__is_active=True,
            status=self.model.Status.CONFIRMED,
        )

    def active_unconfirmed(self):
        return (
            self
            .filter(is_active=True, method_config__is_active=True)
            .exclude(status=self.model.Status.CONFIRMED)
        )


class UserConfig(Timestamped):
    Status = UserConfigStatus
    objects: Union[UserConfigQuerySet, models.Manager] = UserConfigQuerySet.as_manager()

    class Meta:
        verbose_name = pgettext_lazy('wcd_2factor:models', 'User config')
        verbose_name_plural = pgettext_lazy(
            'wcd_2factor:models', 'User config'
        )

    title = models.CharField(
        verbose_name=pgettext_lazy('wcd_2factor:models', 'Title'),
        max_length=1024, blank=True, null=False,
    )
    method_config = models.ForeignKey(
        to=MethodConfig, on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('wcd_2factor:models', 'Method'),
        related_name='wcd_2factor_user_connection_states',
    )
    user = models.ForeignKey(
        dj_settings.AUTH_USER_MODEL,
        verbose_name=pgettext_lazy('wcd_2factor:models', 'User'),
        on_delete=models.CASCADE,
        related_name='wcd_2factor_user_connection_states',
    )
    status = models.CharField(
        verbose_name=pgettext_lazy('wcd_2factor:models', 'Status'),
        max_length=32, choices=Status.choices, default=Status.NEW, db_index=True,
    )
    config = JSONField(
        verbose_name=pgettext_lazy('wcd_2factor:models', 'Config'),
        encoder=get_json_encoder(), default=dict, blank=True, null=False,
    )

    is_active = models.BooleanField(
        pgettext_lazy('wcd_2factor:models', 'Is active'),
        default=True, db_index=True,
    )
    is_default = models.BooleanField(
        pgettext_lazy('wcd_2factor:models', 'Is default'), default=False,
        help_text=pgettext_lazy(
            'wcd_2factor:models',
            'Whether this method should be used as the default the user.'
        ),
    )

    def is_available(self):
        return (
            self.status == self.Status.CONFIRMED
            and
            self.is_active
            and
            self.method_config.is_available()
        )

    def __str__(self):
        return (
            pgettext(
                'wcd_2factor:models',
                '#{method} {status} {title} user #{user} connection.',
            )
            .format(
                method=self.method_config_id,
                status=self.get_status_display(),
                user=self.user_id,
                title=f'"{self.title}"' if self.title else '',
            )
        )

    def get_title(self):
        return self.title or self.method.get_title()
