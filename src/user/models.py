from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ]
    LANGUAGE_CHOICES = [('en', 'English'), ('ua', 'Ukrainian'), ]

    first_name = models.CharField(max_length=11)
    last_name = models.CharField(max_length=11)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=32)
    city = models.CharField(max_length=11)
    card_number = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=13)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='M')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')



