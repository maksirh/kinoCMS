from dateutil.utils import today
from django.shortcuts import render
from django.utils import timezone
from src.cms.models import Banner, Movie
from src.core.adminlte.views import news_and_actions
from src.main.models import MainPage, Page, NewsAndActions


def main_page(request):

    top_banner = Banner.objects.filter(is_active=True, is_promo=True).first()
    movies = Movie.objects.all()

    today = timezone.now().date()

    today_movies = movies.filter(date_of_show__date = today)
    recent_movies = movies.filter(date_of_show__date__gt=today)

    seo = MainPage.objects.first().seo_block

    random_news_or_action = NewsAndActions.objects.order_by('?').first()

    context = {
        "top_banner": top_banner,
        "today_movies": today_movies,
        "recent_movies": recent_movies,
        "seo": seo,
        "news_or_action": random_news_or_action,
    }
    return render(request, "main/main_page.html", context)


def poster(request):

    movies = Movie.objects.all()

    context = {
        "movies": movies,
        "is_active_poster": True,
    }
    return render(request, "main/poster.html", context)



def poster_coming_soon(request):
    today = timezone.now().date()
    recent_movies = Movie.objects.all().filter(date_of_show__date__gt=today)
    context = {
        "movies": recent_movies,
        "is_active_poster_coming_soon": True,
    }

    return render(request, "main/poster.html", context)


def schedule(request):
    return render(request, "main/schedule.html")



def booking(request):
    return render(request, 'main/booking.html')


def schedule_page(request):
    return render(request, 'main/schedule.html')


def news_page(request):
    return  render(request, 'main/news.html')


def cafe_bar_page(request):
    return render(request, 'main/cafe_bar.html')





