from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ManyToManyField

from src.cms.models import SeoBlock, Movie, Hall, Cinema, Gallery
from src.user.models import User
from django.utils import timezone


class MainPage(models.Model):
    phone_number1 = models.CharField(max_length=11)
    phone_number2 = models.CharField(max_length=11)
    seo_text = models.TextField(blank=True, null=True)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Schedule(models.Model):
    id_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    id_hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    id_cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    price = models.FloatField()


class Booking(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    row = models.IntegerField()
    place = models.IntegerField()


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('R', 'Reserved'),
        ('P', 'Paid'),
        ('E', 'Expired'),
    ]

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='tickets')
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='R')
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('schedule', 'row', 'seat')


class Page(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    gallery_images = ManyToManyField(Gallery, blank=True)
    title = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    main_image = models.ImageField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_removable = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


    def delete(self, *args, **kwargs):
        if not self.is_removable:
            raise ValidationError("Не можна видаляти")
        super().delete(*args, **kwargs)


class NewsAndActions(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    gallery_images = ManyToManyField(Gallery, blank=True)
    title = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    main_image = models.ImageField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    video_link = models.URLField(blank=True, null=True)
    is_news = models.BooleanField(default=True)


class DailyStats(models.Model):
    date = models.DateField(unique=True, default=timezone.now)
    sessions = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']







