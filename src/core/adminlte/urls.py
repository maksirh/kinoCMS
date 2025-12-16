from django.urls import path
from .views import (index, banners_top_update, films, banners_edit, news_and_actions_update, through_banner_update,
                    users_list, user_edit, user_delete, pages, main_page)
from django.conf import settings
from django.conf.urls.static import static


app_name = 'adminlte'

urlpatterns = [
    path('', index, name='statistics'),
    path('bannersandsliders/', banners_edit, name='banners'),
    path('banners/top/update/', banners_top_update, name='banners_top_update'),
    path('banners/news/update/', news_and_actions_update, name='news_banner_update'),
    path('baneers/through/update/', through_banner_update, name='banners_through_update'),
    path('banners/', banners_edit, name='films'),
    path('films', films, name='films'),
    path('users/', users_list, name='users_list'),
    path('users/edit/<int:pk>/', user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', user_delete, name='user_delete'),
    path('pages/', pages, name='pages'),
    path('pages/mainpage', main_page, name='main_page'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)