from django.urls import path
from .views import login_user, register, profile, logout_user


app_name = 'authentication'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_user, name='logout'),
]