from django.urls import path
from .views import index, banners_and_sliders, films

app_name = 'adminlte'

urlpatterns = [
    path('', index, name='statistics'),
    path('bannersandsliders', banners_and_sliders, name='banners'),
    path('films', films, name='films'),


]