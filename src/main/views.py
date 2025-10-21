from django.shortcuts import render


def main_page(request):
    return render(request, "main/main_page.html")

def poster(request):
    return render(request, "main/poster.html")

def schedule(request):
    return render(request, "main/schedule.html")



