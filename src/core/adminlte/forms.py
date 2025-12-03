from django import forms
from src.cms.models import BannerComponent, Banner, ThroughBanner, SeoBlock
from src.main.models import MainPage
from django.forms import modelformset_factory


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
                'placeholder': 'Головна сторінка - KinoCMS'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'кіно, квитки, прем\'єри'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Опис для пошукових систем...'
            }),
        }