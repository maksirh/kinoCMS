from django.db import models
from django.forms import FilePathField


class SEO_Block(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=120)
    keywords = models.CharField(max_length=120)
    description = models.TextField()


class Gallery(models.Model):
    image = models.ImageField()


class Movie(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    main_image = models.ImageField()
    trailer_url = models.URLField()
    is_2D = models.BooleanField()
    is_3D = models.BooleanField()
    images = models.ManyToManyField(Gallery)
    seo_block = models.OneToOneField(SEO_Block, on_delete=models.CASCADE)


class Cinema(models.Model):
    seo_block = models.OneToOneField(SEO_Block, on_delete=models.CASCADE)
    gallery_image = models.ManyToManyField(Gallery)
    title = models.CharField(max_length=120)
    description = models.TextField()
    main_image = models.ImageField()
    address = models.CharField(max_length=120)


class Hall(models.Model):
    id_cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    gallery_image = models.ManyToManyField(Gallery)
    seo_block = models.OneToOneField(SEO_Block, on_delete=models.CASCADE)
    number = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField()
    banner_image = models.ImageField()


class BannerComponent(models.Model):
    image = models.ImageField()
    text = models.TextField()
    url = models.URLField()


class Banner(models.Model):
    banner_component = models.ManyToManyField(BannerComponent)
    speed = models.IntegerField()
    is_active = models.BooleanField()
    is_promo = models.BooleanField()


class ThroughBanner(models.Model):
    banner_component = models.ManyToManyField(BannerComponent)
    is_active = models.BooleanField()
    background = models.CharField()


class ContactComponent(models.Model):
    cinema_name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()
    email = models.EmailField()
    is_active = models.BooleanField()


class Contacts(models.Model):
    component = models.ManyToManyField(ContactComponent)
    seo_block = models.OneToOneField(SEO_Block, on_delete=models.CASCADE)


class Mailing(models.Model):
    html_template = FilePathField()
    date = models.DateTimeField()



