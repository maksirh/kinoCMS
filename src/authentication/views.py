from django.shortcuts import render, redirect
from ..user.models import User

def login(request):
    return render(request, 'authentication/auth_page.html')


def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        address = request.POST.get('address').strip()
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
                                        city=city,
                                        card_number=card_number,
                                        phone_number=phone_number,
                                        gender=gender,
                                        language=language)

        return redirect('authentication:login')

    return render(request, 'authentication/register_page.html',)

