from django.db import models
from django.forms import FilePathField
from django.utils import timezone
from django.core.exceptions import ValidationError
import os


class SeoBlock(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=120)
    keywords = models.CharField(max_length=120)
    description = models.TextField()


class Gallery(models.Model):
    image = models.ImageField(upload_to='cinema_gallery/')


class Movie(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    main_image = models.ImageField(upload_to='movies_main/')
    trailer_url = models.URLField()
    is_2D = models.BooleanField()
    is_3D = models.BooleanField()
    date_of_show = models.DateTimeField(default=timezone.now)
    date_of_end_show = models.DateTimeField(default=timezone.now, null=True, blank=True)
    images = models.ManyToManyField(Gallery)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)


class Cinema(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    gallery_image = models.ManyToManyField(Gallery)
    title = models.CharField(max_length=120)
    description = models.TextField()
    main_image = models.ImageField()
    address = models.CharField(max_length=120)


class Hall(models.Model):
    id_cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    gallery_image = models.ManyToManyField(Gallery)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True, blank=True)
    number = models.CharField(max_length=120)
    description = models.TextField()
    scheme_of_hall = models.FileField(upload_to='schemes_hall/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='halls_banners/', null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True, blank=True, null=True)
    is_removable = models.BooleanField(default=True)


    def delete(self, *args, **kwargs):
        if not self.is_removable:
            raise ValidationError("Не можна видаляти")
        super().delete(*args, **kwargs)



class BannerComponent(models.Model):
    image = models.ImageField(upload_to="banners/", blank=True)
    text = models.TextField(blank=True)
    url = models.URLField()


class Banner(models.Model):
    banner_component = models.ManyToManyField(BannerComponent, related_name="banners", blank=True)
    speed = models.IntegerField()
    is_active = models.BooleanField()
    is_promo = models.BooleanField()



class ThroughBanner(models.Model):
    banner_component = models.ManyToManyField(BannerComponent)
    is_active = models.BooleanField()
    background = models.CharField()


class ContactComponent(models.Model):
    logo = models.ImageField(upload_to='contacts/', blank=True)
    cinema_name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()
    email = models.EmailField()
    is_active = models.BooleanField()


class Contacts(models.Model):
    component = models.ManyToManyField(ContactComponent)
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


class Mailing(models.Model):
    subject = models.CharField(max_length=256, default="Новини кінотеатру")
    template_file = models.FileField(upload_to='mailing_templates/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def filename(self):
        return os.path.basename(self.template_file.name)

    class Meta:
        ordering = ['-created_at']


