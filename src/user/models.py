from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ]
    LANGUAGE_CHOICES = [('en', 'English'), ('ua', 'Ukrainian'), ]

    first_name = models.CharField(max_length=11, blank=True)
    last_name = models.CharField(max_length=11, blank=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=11, blank=True)
    card_number = models.CharField(max_length=16, blank=True)
    phone_number = models.CharField(max_length=13, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='M', blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en', blank=True)



