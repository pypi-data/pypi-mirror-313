from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = ('TwoFactorConfig',)


class TwoFactorConfig(AppConfig):
    name = 'wcd_2factor'
    verbose_name = pgettext_lazy('wcd_2factor', 'Two factor')

    def ready(self):
        self.module.autodiscover()
