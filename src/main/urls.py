from django.urls import path
from .views import main_page, poster, booking, schedule, news_page, actions_page, new_and_action, page, poster_coming_soon, filter_schedule, get_halls

app_name = 'main'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('poster/', poster, name='poster'),
    path('poster/comingsoon', poster_coming_soon, name='poster_coming_soon'),
    path('filter-schedule/', filter_schedule, name='filter_schedule'),
    path('get-halls/', get_halls, name='get_halls'),
    path('booking/<int:schedule_id>', booking, name='booking'),
    path('schedule/', schedule, name='schedule_page'),
    path('news/', news_page, name='news_page'),
    path('actions/', actions_page, name='actions_page'),
    path('news_actions/<int:item_pk>', new_and_action, name='new_and_action_page'),
    path('page/<int:page_id>', page, name='page'),

]


