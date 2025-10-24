from django.shortcuts import render


def login(request):
    return render(request, 'authentication/auth_page.html')