from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..user.models import User


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main:main_page')

        else:
            messages.error(request, 'Username OR password is incorrect')


    return render(request, 'authentication/auth_page.html', {})


def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        address = request.POST.get('address').strip()
        country = request.POST.get('country')
        city = request.POST.get('city')
        card_number = request.POST.get('card-number').strip()
        phone_number = request.POST.get('phone_number').strip()
        gender = request.POST.get('gender')
        language = request.POST.get('language')

        user = User.objects.create_user(first_name=first_name,
                                        last_name=last_name,
                                        username=username,
                                        email=email,
                                        password=password,
                                        address=address,
                                        country=country,
                                        city=city,
                                        card_number=card_number,
                                        phone_number=phone_number,
                                        gender=gender,
                                        language=language)

        return redirect('authentication:login')

    return render(request, 'authentication/register_page.html',)


def profile(request):
    return render(request, 'authentication/profile.html')
