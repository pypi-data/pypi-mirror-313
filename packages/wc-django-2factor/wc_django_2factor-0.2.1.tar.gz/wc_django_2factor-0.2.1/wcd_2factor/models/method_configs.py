from typing import *
from django.db import models
from django.utils.translation import pgettext_lazy

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

from django.utils.translation import pgettext_lazy
from django.db import models
from wcd_settings.utils.dynamic_choices_field import DynamicChoicesField
from wcd_settings.utils.descriptor_registry import registry_choices

from .base import Timestamped
from ..utils import get_json_encoder


__all__ = 'MethodConfig',


class MethodConfigQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class MethodConfig(Timestamped):
    objects: Union[MethodConfigQuerySet, models.Manager] = MethodConfigQuerySet.as_manager()

    class Meta:
        verbose_name = pgettext_lazy('wcd_2factor:models', 'Method config')
        verbose_name_plural = pgettext_lazy('wcd_2factor:models', 'Method config')

    title = models.CharField(
        verbose_name=pgettext_lazy('wcd_2factor:models', 'Title'),
        max_length=1024, blank=True, null=False,
    )
    method = DynamicChoicesField(
        verbose_name=pgettext_lazy('wcd_2factor:models', 'Method'),
        choices=registry_choices(
            'wcd_2factor.registries.method_config_registry'
        ),
        max_length=128, blank=False, null=False, db_index=True,
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
            'Whether this method should be used as the default for all users.'
        ),
    )

    def __str__(self):
        return self.get_title()

    def get_title(self):
        return self.title or self.get_method_display()

    def is_available(self):
        return self.is_active
