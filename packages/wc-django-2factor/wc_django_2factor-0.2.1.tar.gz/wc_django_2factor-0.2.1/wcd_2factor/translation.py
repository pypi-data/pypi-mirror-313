from modeltranslation.translator import register, TranslationOptions

from .models import MethodConfig


@register(MethodConfig)
class MethodConfigTranslationOptions(TranslationOptions):
    fields = 'title',
