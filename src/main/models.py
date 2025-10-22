from django.db import models
from django.db.models import ManyToManyField

from src.cms.models import SeoBlock, Movie, Hall, Cinema, Gallery
from src.user.models import User


class MainPage(models.Model):
    phone_number1 = models.CharField(max_length=11)
    phone_number2 = models.CharField(max_length=11)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)


class Schedule(models.Model):
    id_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    id_hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    id_cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.FloatField()


class Booking(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    row = models.IntegerField()
    place = models.IntegerField()


class Page(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    gallery_image = ManyToManyField(Gallery)
    title = models.CharField(max_length=120)
    description = models.TextField()
    main_image = models.ImageField()
    is_active = models.BooleanField()





