from django.shortcuts import render


def register(request):
    return render(request, 'user/register_page.html')
