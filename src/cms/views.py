from django.shortcuts import render, get_object_or_404
from src.cms.models import Cinema, Hall
from src.main.models import Schedule
from django.utils import timezone

def cinemas_list(request):
    
    cinemas = Cinema.objects.all()

    context = {
        "cinemas": cinemas
    }
    return render(request, 'cms/cinemas.html', context)


def cinema_page(request, cinema_id):

    cinema = get_object_or_404(Cinema, pk=cinema_id)
    halls = Hall.objects.all().filter(id_cinema=cinema)
    today_sessions = Schedule.objects.all().filter(id_cinema=cinema, date__date=timezone.now())


    context = {
        "cinema": cinema,
        "halls": halls,
        "today_sessions": today_sessions,

    }

    return render(request, 'cms/cinema.html', context)
