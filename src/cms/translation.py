from modeltranslation.translator import register, TranslationOptions
from .models import ContactComponent, SeoBlock, Movie, Cinema, Hall


@register(ContactComponent)
class ContactComponentTranslationOptions(TranslationOptions):
    fields = ('cinema_name', 'address')

@register(SeoBlock)
class SeoBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'keywords', 'description')

@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address')

@register(Hall)
class HallTranslationOptions(TranslationOptions):
    fields = ('description',)