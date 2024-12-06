from django.utils.translation import pgettext_lazy


class TwoFactorError(Exception):
    pass


class ConfirmationFailed(TwoFactorError):
    pass


class MethodMissing(TwoFactorError):
    method: str

    def __init__(self, method):
        self.method = method

    def __str__(self):
        return pgettext_lazy(
            'wcd_2factor:error',
            'Incorrect 2factor method: "{method}".'
        ).format(method=self.method)
