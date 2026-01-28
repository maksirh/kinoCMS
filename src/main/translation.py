from modeltranslation.translator import register, TranslationOptions
from .models import NewsAndActions, Page, MainPage


@register(NewsAndActions)
class NewsAndActionsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(MainPage)
class MainPageTranslationOptions(TranslationOptions):
    fields = ('seo_text',)
