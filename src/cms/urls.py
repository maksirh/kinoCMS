from django.urls import path
from .views import cinema_page, cinemas_list, hall_page, contacts_list

app_name = 'cinema'

urlpatterns = [
    path('cinemas', cinemas_list, name='cinemas_list'),
    path('cinema/<int:cinema_id>/', cinema_page, name="cinema_page"),
    path('hall/<int:hall_id>', hall_page, name="hall_page"),
    path('contacts', contacts_list, name='contacts_list'),
]