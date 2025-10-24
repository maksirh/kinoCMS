from django.urls import path
from .views import register

app_name = 'user'

urlpatterns = [
    path('register/', register, name='register'),
]