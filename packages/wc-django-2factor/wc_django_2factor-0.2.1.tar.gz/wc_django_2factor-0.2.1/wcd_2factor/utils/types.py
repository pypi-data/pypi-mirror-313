from typing import *

from zoneinfo import ZoneInfo
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

from .functional import autoimport


__all__ = 'get_json_encoder', 'TwoFactorJSONEncoder',


def get_json_encoder():
    from ..conf import settings

    return autoimport(settings.JSON_ENCODER)


class TwoFactorJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ZoneInfo):
            return o.key
        elif isinstance(o, models.Model):
            from django.contrib.contenttypes.models import ContentType

            return {
                'content_type': ContentType.objects.get_for_model(o.__class__),
                'pk': o.pk,
                'display': str(o),
            }
        elif isinstance(o, Exception):
            return str(o)
        else:
            return super().default(o)
