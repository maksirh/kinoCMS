from django.urls import path
from .views import main_page, poster, booking, schedule_page, news_page, cafe_bar_page, poster_coming_soon

app_name = 'main'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('poster/', poster, name='poster'),
    path('poster/comingsoon', poster_coming_soon, name='poster_coming_soon'),
    path('booking/', booking, name='booking'),
    path('schedule/', schedule_page, name='schedule_page'),
    path('news/', news_page, name='news_page'),
    path('cafe', cafe_bar_page, name='cafe_bar_page'),

]


