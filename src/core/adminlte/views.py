from django.shortcuts import render

def index(request):
    return render(request, 'adminlte/dashboard.html')


def banners_and_sliders(request):
    return render(request, 'adminlte/banners_edit.html')


def films(request):
    return render(request, 'adminlte/films.html')

