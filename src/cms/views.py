from django.shortcuts import render

def cinema_page(request):
    return render(request, 'cms/cinema.html')
