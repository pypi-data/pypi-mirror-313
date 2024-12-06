from typing import *

from django.db import models
from rest_framework import serializers


__all__ = 'CallableQuerySetMixin', 'PrimaryKeyRelatedField',


class CallableQuerySetMixin:
    def get_queryset(self):
        queryset = self.queryset

        if callable(queryset):
            queryset = queryset(self)

        if isinstance(queryset, (models.QuerySet, models.Manager)):
            queryset = queryset.all()

        return queryset


class PrimaryKeyRelatedField(CallableQuerySetMixin, serializers.PrimaryKeyRelatedField):
    pass
