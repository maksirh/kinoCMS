from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..user.models import User
from .forms import UserRegistrationForm, UserUpdateForm


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


def logout_user(request):
    logout(request)
    return redirect('main:main_page')




def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authentication:login')

        else:
            print(form.errors)
            messages.error(request, 'Error')

    else:
        form = UserRegistrationForm()

    return render(request, 'authentication/register_page.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        print("POST keys:", list(request.POST.keys()))
        print("is_valid:", form.is_valid())
        print("errors:", form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль оновлено")
            return redirect("authentication:profile")
        messages.error(request, "Перевірте форму, є помилки.")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "authentication/profile.html", {"form": form})




