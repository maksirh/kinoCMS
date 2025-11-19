from django.urls import path
from .views import index, banners_top_update, films, banners_edit, news_and_actions_update
from django.conf import settings
from django.conf.urls.static import static


app_name = 'adminlte'

urlpatterns = [
    path('', index, name='statistics'),
    path('bannersandsliders/', banners_edit, name='banners'),
    path('banners/top/update/', banners_top_update, name='banners_top_update'),
    path('banners/news/update/', news_and_actions_update, name='news_banner_update'),
    path('banners/', banners_edit, name='films'),
    path('films', films, name='films'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)