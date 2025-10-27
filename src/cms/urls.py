from django.urls import path
from .views import cinema_page

app_name = 'cinema'

urlpatterns = [
    path('cinemas', cinema_page, name='cinema_page'),
]