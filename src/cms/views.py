from django.shortcuts import render, get_object_or_404
from src.cms.models import Cinema


def cinemas_list(request):
    
    cinemas = Cinema.objects.all()

    context = {
        "cinemas": cinemas
    }
    return render(request, 'cms/cinemas.html', context)


def cinema_page(request, cinema_id):

    cinema = get_object_or_404(Cinema, pk=cinema_id)

    context = {
        "cinema": cinema,
    }

    return render(request, 'cms/cinema.html', context)
