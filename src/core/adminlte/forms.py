from django import forms
from src.cms.models import BannerComponent, Banner
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



BannerComponentFormSet = modelformset_factory(
    BannerComponent,
    form=BannerComponentForm,
    extra=0,
    can_delete=True
)