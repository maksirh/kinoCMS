from django import forms
from src.cms.models import BannerComponent, Banner, ThroughBanner, SeoBlock, Movie, Cinema, ContactComponent, Contacts, \
    Hall, Mailing
from src.main.models import MainPage, Page, Gallery, NewsAndActions, Schedule
from django.forms import modelformset_factory
import json
from django.core.exceptions import ValidationError


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ["speed", "is_active"]


class BannerComponentForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"accept": "image/*"}))
    text = forms.CharField(required=False, widget=forms.Textarea)
    class Meta:
        model = BannerComponent
        fields = ["image", "url", "text"]


class ThroughBannerForm(forms.ModelForm):
    class Meta:
        model = ThroughBanner
        fields = ["is_active", "background"]
        widgets = {
            'background': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color',
                'title': 'Оберіть колір фону'
            }),
        }


class SimpleImageComponentForm(forms.ModelForm):
    class Meta:
        model = BannerComponent
        fields = ["image"]

ThroughBannerFormSet = modelformset_factory(
    BannerComponent,
    form=SimpleImageComponentForm,
    extra=1,
    max_num=1,
    validate_max=True,
    can_delete=False
)


ThroughBannerFormSet = modelformset_factory(
    BannerComponent,
    form=SimpleImageComponentForm,
    extra=1,
    max_num=1,
    validate_max=True,
    can_delete=False
)


BannerComponentFormSet = modelformset_factory(
    BannerComponent,
    form=BannerComponentForm,
    extra=0,
    can_delete=True
)


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ['phone_number1',
                  'phone_number2',
                  'seo_text_uk', 'seo_text_en']

        widgets = {
            'phone_number1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '777 85 98'}),
            'phone_number2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '777 85 98'}),

            'seo_text_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введіть SEO текст для головної сторінки...'
            }),

            'seo_text_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter SEO text for main page...'
            }),
        }


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title_uk', 'title_en',
                  'description_uk', 'description_en',
                  'main_image', 'is_active']
        widgets = {
            'title_uk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'О кинотеатре'}),
            'title_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'About cinema'}),
            'description_uk': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Текст'}),
            'description_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Text'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control d-none', 'id': 'mainImageInput'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = [
            'url',
            'title_uk', 'title_en',
            'keywords_uk', 'keywords_en',
            'description_uk', 'description_en'
        ]
        widgets = {
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'example-page-url'
            }),

            'title_uk': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок сторінки (UA)'
            }),
            'keywords_uk': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ключові слова (UA)'
            }),
            'description_uk': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Опис для пошукових систем (UA)'
            }),


            'title_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Page Title (EN)'
            }),
            'keywords_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Keywords (EN)'
            }),
            'description_en': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description for search engines (EN)'
            }),
        }

GalleryFormSet = modelformset_factory(
    Gallery,
    fields=('image',),
    extra=1,
    can_delete=True,
    widgets={
        'image': forms.FileInput(attrs={'class': 'd-none gallery-input', 'onchange': 'previewGalleryImage(this)'})
    }
)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title_uk', 'title_en',
            'description_uk', 'description_en',
            'main_image', 'trailer_url',
            'is_2D', 'is_3D',
            'date_of_show', 'date_of_end_show'
        ]

        widgets = {

            'title_uk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва фільму (UA)'}),
            'description_uk': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опис (UA)'}),

            'title_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie Title (EN)'}),
            'description_en': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description (EN)'}),

            'main_image': forms.FileInput(attrs={'class': 'form-control d-none', 'id': 'mainImageInput'}),
            'trailer_url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_2D': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_3D': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_of_show': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'date_of_end_show': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.date_of_show:
                self.fields['date_of_show'].initial = self.instance.date_of_show.strftime('%Y-%m-%dT%H:%M')
            if self.instance.date_of_end_show:
                self.fields['date_of_end_show'].initial = self.instance.date_of_end_show.strftime('%Y-%m-%dT%H:%M')


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = [
            'title_uk', 'title_en',
            'description_uk', 'description_en',
            'address_uk', 'address_en',
            'main_image', 'phone_number', 'email'
        ]

        widgets = {
            'title_uk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва (UA)'}),
            'title_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name (EN)'}),

            'description_uk': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опис (UA)'}),
            'description_en': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description (EN)'}),

            'address_uk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адреса (UA)'}),
            'address_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address (EN)'}),

            'main_image': forms.FileInput(attrs={'class': 'form-control', 'id': 'logoInput'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ContactComponentForm(forms.ModelForm):
    class Meta:
        model = ContactComponent
        fields = [
            'logo',
            'cinema_name_uk', 'cinema_name_en',
            'address_uk', 'address_en',
            'phone_number', 'latitude', 'longitude', 'email', 'is_active'
        ]
        widgets = {
            'logo': forms.FileInput(attrs={'class': 'd-none'}),

            'cinema_name_uk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва (UA)'}),
            'address_uk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адреса (UA)'}),

            'cinema_name_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name (EN)'}),
            'address_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address (EN)'}),

            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


ContactComponentFormset = modelformset_factory(
    ContactComponent,
    form = ContactComponentForm,
    extra=0,
    can_delete=True,

)


class HallForm(forms.ModelForm):
    scheme_of_hall = forms.FileField(
        label="Схема залу (JSON)",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'd-none',
            'accept': '.json,application/json',
            'id': 'id_scheme_of_hall'
        })
    )

    class Meta:
        model = Hall
        fields = ['number',
                  'description_uk', 'description_en',
                  'scheme_of_hall', 'banner_image']

        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'description_uk': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'banner_image': forms.FileInput(attrs={'class': 'd-none'}),
        }

    def clean_scheme_of_hall(self):
        scheme_file = self.cleaned_data.get('scheme_of_hall')

        if not scheme_file:
            if self.instance.pk:
                return self.instance.scheme_of_hall
            return None


        if hasattr(scheme_file, 'read'):
            try:
                json.load(scheme_file)

                scheme_file.seek(0)

            except json.JSONDecodeError:
                raise ValidationError("Файл містить помилки або не є форматом JSON")

        return scheme_file


class NewsAndActionsForm(forms.ModelForm):
    class Meta:
        model = NewsAndActions
        fields = ['title_uk', 'title_en',
                  'description_uk', 'description_en',
                  'main_image', 'is_active', 'video_link']

        widgets = {
            'title_uk': forms.TextInput(attrs={'class': 'form-control'}),
            'title_en': forms.TextInput(attrs={'class': 'form-control'}),
            'description_uk': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'main_image': forms.FileInput(attrs={'class': 'd-none'}),
            'video_link': forms.URLInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['template_file']
        widgets = {
            'template_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.html'}),
        }
        

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['id_cinema', 'id_hall', 'id_movie', 'date', 'price']
        labels = {
            'id_cinema': 'Кінотеатр',
            'id_hall': 'Зал',
            'id_movie': 'Фільм',
            'date': 'Дата та час сеансу',
            'price': 'Ціна квитка (грн)',
        }
        widgets = {
            'id_cinema': forms.Select(attrs={'class': 'form-control select2', 'id': 'id_cinema'}),
            'id_hall': forms.Select(attrs={'class': 'form-control select2', 'id': 'id_hall'}),
            'id_movie': forms.Select(attrs={'class': 'form-control select2'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': 'Наприклад: 150.00'}),
        }

