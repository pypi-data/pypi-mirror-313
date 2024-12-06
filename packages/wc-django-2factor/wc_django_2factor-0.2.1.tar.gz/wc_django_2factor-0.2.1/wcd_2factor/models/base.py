from typing import *
from django.db import models
from django.utils.translation import pgettext_lazy

from django.utils.translation import pgettext_lazy
from django.db import models


__all__ = 'Timestamped',


class Timestamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_2factor', 'Created at'),
        auto_now_add=True, blank=False, null=False, db_index=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_2factor', 'Updated at'),
        auto_now=True, blank=False, null=False, db_index=True,
    )
