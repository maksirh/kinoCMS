from django import forms
from src.cms.models import BannerComponent, Banner, ThroughBanner
from django.forms import ModelForm, inlineformset_factory, modelformset_factory


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