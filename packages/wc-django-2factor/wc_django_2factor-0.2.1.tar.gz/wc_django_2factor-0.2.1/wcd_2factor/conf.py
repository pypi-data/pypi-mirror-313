from dataclasses import dataclass, field
from typing import *

from px_settings.contrib.django import settings as setting_wrap

from .const import SETTINGS_PREFIX


__all__ = 'Settings', 'settings',


@setting_wrap(SETTINGS_PREFIX)
@dataclass
class Settings:
    METHODS: Sequence[str] = field(default_factory=list)
    JSON_ENCODER: str = 'wcd_2factor.utils.types.TwoFactorJSONEncoder'


settings = Settings()
