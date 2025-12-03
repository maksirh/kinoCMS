from django import forms
from django.contrib.auth.forms import UserCreationForm

from ..user.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'language',
                  'phone_number', "address", "card_number", "city"]


class UserUpdateForm(forms.ModelForm):
    class Meta():
        model = User

        fields = [
            "email", "first_name", "last_name",
            "phone_number", "address", "city",
            "language", "gender", "card_number",
        ]

        widgets = {
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "address": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-control'}),
            "card_number": forms.TextInput(attrs={'class': 'form-control'}),
            "language": forms.Select(attrs={'class': 'form-control'}),
        }

