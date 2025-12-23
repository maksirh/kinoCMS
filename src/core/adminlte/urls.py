from django.urls import path
from .views import (index, banners_top_update, film_list, banners_edit, news_and_actions_update,
                    through_banner_update, users_list, user_edit, user_delete, pages,
                    main_page, page_add, page_edit, page_delete,
                    edit_mainpage, add_movie, edit_movie, cinemas_list,
                    cinema_add, contacts, edit_cinema, delete_cinema)
from django.conf import settings
from django.conf.urls.static import static


app_name = 'adminlte'

urlpatterns = [
    path('', index, name='statistics'),
    path('bannersandsliders/', banners_edit, name='banners'),
    path('banners/top/update/', banners_top_update, name='banners_top_update'),
    path('banners/news/update/', news_and_actions_update, name='news_banner_update'),
    path('baneers/through/update/', through_banner_update, name='banners_through_update'),
    path('films/', film_list, name='film_list'),
    path('films/add/', add_movie, name='add_movie'),
    path('films/edit/<int:pk>/', edit_movie, name='edit_movie'),
    path('users/', users_list, name='users_list'),
    path('users/edit/<int:pk>/', user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', user_delete, name='user_delete'),
    path('pages/', pages, name='pages'),
    path('pages/mainpage', main_page, name='main_page'),
    path('page/add', page_add, name='add_page'),
    path('page/edit/<int:pk>/', page_edit, name='edit_page'),
    path('page/delete/<int:pk>/', page_delete, name='delete_page'),
    path('page/mainpage/edit', edit_mainpage, name='edit_mainpage'),
    path('page/contacts/edit', contacts, name='contacts'),
    path('cinemas/', cinemas_list, name='cinemas_list'),
    path('cinemas/add/', cinema_add, name='cinema_add'),
    path('cinemas/edit/<int:pk>', edit_cinema, name='edit_cinema'),
    path('cinemas/delete/<int:pk>', delete_cinema, name='cinema_delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)