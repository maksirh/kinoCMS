from django.urls import path
from .views import main_page, poster, booking, schedule_page

app_name = 'main'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('poster/', poster, name='poster'),
    path('booking/', booking, name='booking'),
    path('schedule/', schedule_page, name='schedule_page'),
]


