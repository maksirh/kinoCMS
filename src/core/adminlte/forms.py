from django import forms
from src.cms.models import BannerComponent, Banner, ThroughBanner, SeoBlock, Movie, Cinema, ContactComponent, Contacts, \
    Hall, Mailing
from src.main.models import MainPage, Page, Gallery, NewsAndActions
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
        fields = ['phone_number1', 'phone_number2', 'seo_text']

        widgets = {
            'phone_number1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '777 85 98'}),
            'phone_number2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '777 85 98'}),

            'seo_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введіть SEO текст для головної сторінки...'
            }),
        }


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'description', 'main_image', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'О кинотеатре'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Текст'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control d-none', 'id': 'mainImageInput'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ['url', 'title', 'keywords', 'description']
        widgets = {
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Опис для пошукових систем...'
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
        fields = ['title', 'description', 'main_image', 'trailer_url', 'is_2D', 'is_3D', 'date_of_show', 'date_of_end_show']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'main_image': forms.FileInput(attrs={'class': 'form-control', 'id': 'mainImageInput'}),
            'trailer_url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_2D': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_3D': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_of_show': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'date_of_end_show': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.date_of_show:
            self.fields['date_of_show'].widget.attrs['value'] = self.instance.date_of_show.strftime('%Y-%m-%dT%H:%M')



class CinemaForm(forms.ModelForm):

    class Meta:
        model = Cinema
        fields = ['title', 'description', 'main_image', 'address']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'main_image': forms.FileInput(attrs={'class': 'form-control', 'id': 'logoInput'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ContactComponentForm(forms.ModelForm):
    class Meta:
        model = ContactComponent
        fields = ['logo', 'cinema_name', 'address', 'phone_number', 'latitude', 'longitude', 'email', 'is_active']
        widgets = {
            'logo': forms.FileInput(attrs={'class': 'd-none'}),
            'cinema_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
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
        fields = ['number', 'description', 'scheme_of_hall', 'banner_image']

        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
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
        fields = ['title', 'description', 'main_image', 'is_active', 'video_link']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
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
        


