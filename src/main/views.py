from dateutil.utils import today
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from src.cms.models import Banner, Movie, ThroughBanner
from src.main.models import MainPage, Page, NewsAndActions, Hall, Schedule, Cinema, Ticket
from django.http import JsonResponse
from django.template.loader import render_to_string


def main_page(request):

    top_banner = Banner.objects.filter(is_active=True, is_promo=True).first()
    movies = Movie.objects.all()

    today = timezone.now().date()

    current_movies = movies.filter(date_of_show__date__lte=today, date_of_end_show__date__gte=today)
    recent_movies = movies.filter(date_of_show__date__gt=today)

    seo = MainPage.objects.first().seo_block

    news_or_action = Banner.objects.filter(is_active=True, is_promo=False).first()

    through_banner = ThroughBanner.objects.first()

    context = {
        "top_banner": top_banner,
        "today_movies": current_movies,
        "recent_movies": recent_movies,
        "seo": seo,
        "news_or_actions": news_or_action,
        "through_banner": through_banner,
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


def get_halls(request):
    cinema_id = request.GET.get('cinema_id')
    halls = Hall.objects.filter(id_cinema_id=cinema_id).values('id', 'number')
    return JsonResponse(list(halls), safe=False)


def filter_schedule(request):
    cinema_id = request.GET.get('cinema')
    hall_id = request.GET.get('hall')
    date = request.GET.get('date')

    schedules = Schedule.objects.all()

    if cinema_id:
        schedules = schedules.filter(id_cinema_id=cinema_id)
    if hall_id:
        schedules = schedules.filter(id_hall_id=hall_id)
    if date:
        schedules = schedules.filter(date__date=date)

    html = render_to_string('main/partials/schedule_rows.html', {'schedules': schedules})
    return JsonResponse({'html': html})


def schedule(request):
    context = {
        'cinemas': Cinema.objects.all(),
        'movies': Movie.objects.all(),
        'schedules': Schedule.objects.all()[:10],
    }
    return render(request, "main/schedule.html", context)



def booking(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    booked_tickets = Ticket.objects.filter(schedule=schedule).exclude(status="E")

    context = {
        'schedule': schedule,
        'booked_tickets': booked_tickets,
        'hall_scheme': schedule.id_hall.scheme_of_hall
    }

    return render(request, 'main/booking.html', context)



def news_page(request):
    top_banner = Banner.objects.filter(is_active=True, is_promo=True).first()
    news = NewsAndActions.objects.all().filter(is_news=True)

    context = {
        "top_banner": top_banner,
        "items": news,
    }

    return render(request, "main/news_and_actions.html", context)


def actions_page(request):
    top_banner = Banner.objects.filter(is_active=True, is_promo=True).first()
    actions = NewsAndActions.objects.all().filter(is_news=False)

    context = {
        "top_banner": top_banner,
        "items": actions,
    }

    return render(request, "main/news_and_actions.html", context)


def new_and_action(request, item_pk):
    top_banner = Banner.objects.filter(is_active=True, is_promo=True).first()
    news_or_action = get_object_or_404(NewsAndActions, id=item_pk)

    context = {
        "item": news_or_action,
        "top_banner": top_banner
    }

    return  render(request, 'main/news_or_action.html', context)




def cafe_bar_page(request):
    return render(request, 'main/cafe_bar.html')





