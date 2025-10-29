from django.urls import path
from . import views

app_name = 'adminlte'

urlpatterns = [
    path('', views.index, name='statistics'),
    path('bannersandsliders', views.banners_and_sliders, name='banners'),



]