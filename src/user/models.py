from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=11)
    last_name = models.CharField(max_length=11)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=32)
    city = models.CharField(max_length=11)
    card_number = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=13)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ua', 'Ukrainian'),
    ]



