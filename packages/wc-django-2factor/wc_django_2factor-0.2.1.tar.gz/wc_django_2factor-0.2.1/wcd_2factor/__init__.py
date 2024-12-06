__version__ = '0.2.1'

VERSION = tuple(__version__.split('.'))

default_app_config = 'wcd_2factor.apps.TwoFactorConfig'


def autodiscover():
    from wcd_2factor.registries import method_config_registry
    from wcd_2factor.utils import autoimport
    from wcd_2factor.conf import settings

    method_config_registry.multiregister(
        [autoimport(m) for m in settings.METHODS],
    )
