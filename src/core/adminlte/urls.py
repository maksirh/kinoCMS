from django.urls import path
from .views import index, banners_and_sliders, films
from django.conf import settings
from django.conf.urls.static import static


app_name = 'adminlte'

urlpatterns = [
    path('', index, name='statistics'),
    path('bannersandsliders', banners_and_sliders, name='banners'),
    path('films', films, name='films'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)