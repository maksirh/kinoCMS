from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from src.cms.models import BannerComponent, ThroughBanner, Contacts, Hall
from src.user.models import User
from src.main.models import DailyStats
from django.contrib.auth import get_user_model
from src.authentication.forms import UserUpdateForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .tasks import send_mass_mail_task
import datetime
import json
from django.db.models import Count



def banners_edit(request):
    banner_top = Banner.objects.order_by('pk').filter(is_promo=True).first()
    if banner_top is None:
        banner_top = Banner.objects.create(speed=5, is_active=True, is_promo=True)

    banner_news = Banner.objects.order_by('pk').filter(is_promo=False).first()
    if banner_news is None:
        banner_news = Banner.objects.create(speed=5, is_active=True, is_promo=False)

    banner_through = ThroughBanner.objects.first()
    if banner_through is None:
        banner_through = ThroughBanner.objects.create(is_active=True, background="#FFFFFF")

    form_top = BannerForm(instance=banner_top, prefix="top_main")
    formset_top = BannerComponentFormSet(queryset=banner_top.banner_component.all(), prefix='top_items')

    form_news = BannerForm(instance=banner_news, prefix="news_main")
    formset_news = BannerComponentFormSet(queryset=banner_news.banner_component.all(), prefix='news_items')

    form_through = ThroughBannerForm(instance=banner_through, prefix="through_main")

    formset_through = ThroughBannerFormSet(
        queryset=banner_through.banner_component.all(),
        prefix='through_items'
    )

    return render(request, "adminlte/banners_edit.html", {
        "form_top": form_top,
        "formset_top": formset_top,
        "form_news": form_news,
        "formset_news": formset_news,

        "form_through": form_through,
        "formset_through": formset_through,
    })


def through_banner_update(request):
    banner = ThroughBanner.objects.first()
    if not banner:
        banner = ThroughBanner.objects.create(is_active=True, background="#FFFFFF")

    if request.method == "POST":
        form = ThroughBannerForm(request.POST, instance=banner, prefix="through_main")

        formset = ThroughBannerFormSet(
            request.POST, request.FILES,
            queryset=banner.banner_component.all(),
            prefix="through_items"
        )

        if form.is_valid() and formset.is_valid():
            banner_instance = form.save()

            instances = formset.save(commit=False)
            for comp in instances:
                comp.save()
                banner_instance.banner_component.clear()
                banner_instance.banner_component.add(comp)

            return redirect("adminlte:banners")
        else:
            print("Through Banner Errors:", form.errors, formset.errors)

    else:
        form = ThroughBannerForm(instance=banner, prefix="through_main")
        formset = ThroughBannerFormSet(
            queryset=banner.banner_component.all(),
            prefix="through_items"
        )

    return render(request, "adminlte/through_banner_edit.html", {
        "form_through": form,
        "formset_through": formset,
    })

def banners_top_update(request):
    banner = Banner.objects.order_by('pk').filter(is_promo=True).first()
    if not banner:
        banner = Banner.objects.create(speed=5, is_active=True, is_promo=True)

    if request.method == "POST":
        form = BannerForm(request.POST, instance=banner, prefix="top_main")
        formset = BannerComponentFormSet(
            request.POST, request.FILES,
            queryset=banner.banner_component.all(),
            prefix="top_items"
        )

        if form.is_valid() and formset.is_valid():
            banner_instance = form.save()

            for f in formset.deleted_forms:
                comp = f.instance
                if comp.pk:
                    banner_instance.banner_component.remove(comp)

                    comp.delete()

            instances = formset.save(commit=False)
            for comp in instances:
                comp.save()
                banner_instance.banner_component.add(comp)

            return redirect("adminlte:banners")
        else:
            print("TOP Errors:", form.errors, formset.errors)

    return redirect("adminlte:banners")


def news_and_actions_update(request):
    banner = Banner.objects.order_by('pk').filter(is_promo=False).first()
    if not banner:
        banner = Banner.objects.create(speed=5, is_active=True, is_promo=False)

    if request.method == "POST":
        form = BannerForm(request.POST, instance=banner, prefix="news_main")
        formset = BannerComponentFormSet(
            request.POST, request.FILES,
            queryset=banner.banner_component.all(),
            prefix="news_items"
        )

        if form.is_valid() and formset.is_valid():
            banner_instance = form.save()

            for f in formset.deleted_forms:
                comp = f.instance
                if comp.pk:
                    banner_instance.banner_component.remove(comp)
                    comp.delete()

            instances = formset.save(commit=False)
            for comp in instances:
                comp.save()
                banner_instance.banner_component.add(comp)

            return redirect("adminlte:banners")
        else:
             print("NEWS Errors:", form.errors, formset.errors)

    return redirect("adminlte:banners")


def film_list(request):
    now = timezone.now()

    current_movies = Movie.objects.filter(date_of_show__lte=now).order_by('-date_of_show')
    soon_movies = Movie.objects.filter(date_of_show__gt=now).order_by('date_of_show')

    contex = {
        'current_movies': current_movies,
        'soon_movies': soon_movies,
    }

    return render(request, 'adminlte/film_list.html', contex)


User = get_user_model()

def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Користувача {user_obj.username} оновлено!')
            return redirect('adminlte:users_list')
    else:
        form = UserUpdateForm(instance=user_obj)

    context = {
        'form': form,
        'user_obj': user_obj
    }
    return render(request, 'adminlte/user_edit.html', context)

def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        username = user_obj.username
        user_obj.delete()
        messages.warning(request, f'Користувача {username} видалено.')
        return redirect('adminlte:users_list')

    return redirect('adminlte:users_list')


def users_list(request):
    queryset = User.objects.all().order_by('-date_joined')

    search_query = request.GET.get('q')

    if search_query:
        queryset = queryset.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    paginator = Paginator(queryset, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'adminlte/users_list.html', context)


def main_page(request):
    main_page_obj, created = MainPage.objects.get_or_create(id=1)

    if not main_page_obj.seo_block:
        seo_block_obj = SeoBlock.objects.create()
        main_page_obj.seo_block = seo_block_obj
        main_page_obj.save()
    else:
        seo_block_obj = main_page_obj.seo_block

    if request.method == 'POST':
        main_form = MainPageForm(request.POST, instance=main_page_obj)
        seo_form = SeoBlockForm(request.POST, instance=seo_block_obj)

        if main_form.is_valid() and seo_form.is_valid():
            main_form.save()
            seo_form.save()
            return redirect('adminlte:main_page')
    else:
        main_form = MainPageForm(instance=main_page_obj)
        seo_form = SeoBlockForm(instance=seo_block_obj)

    context = {
        'main_form': main_form,
        'seo_form': seo_form,
    }
    return render(request, 'adminlte/main_page.html', context)



def pages(request):
    main_page = MainPage.load()
    contacts = Contacts.load()
    pages = Page.objects.all().order_by('id')
    context = {
        "main_page": main_page,
        "pages": pages,
        "contacts": contacts,
    }

    return render(request, 'adminlte/pages.html', context)


def page_add(request):

    if request.method == 'POST':

        page_form = PageForm(request.POST, request.FILES)
        seo_form = SeoBlockForm(request.POST)

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=Gallery.objects.none(),
            prefix='gallery',
        )

        if page_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():
            seo_block = seo_form.save()
            page = page_form.save(commit=False)
            page.seo_block = seo_block
            page.save()

            new_images = gallery_formset.save()

            if new_images:
                page.gallery_images.add(*new_images)

            return redirect('adminlte:pages')
    else:
        page_form = PageForm()
        seo_form = SeoBlockForm()
        gallery_formset = GalleryFormSet(
            queryset=Gallery.objects.none(),
            prefix='gallery'
        )

    context = {
        'page_form': page_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
    }

    return render(request, 'adminlte/page.html', context)





def page_edit(request, pk):

    page = get_object_or_404(Page, pk=pk)

    seo_instance = page.seo_block

    if request.method == 'POST':
        page_form = PageForm(request.POST, request.FILES, instance=page)
        seo_form = SeoBlockForm(request.POST, instance=seo_instance, prefix='seo')

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=page.gallery_images.all(),
            prefix='gallery',
        )

        if page_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():
            seo_block = seo_form.save()
            page = page_form.save(commit=False)

            if request.POST.get('clear_main_image') == 'true':
                page.main_image.delete(save=False)
                page.main_image = None

            page.seo_block = seo_block
            page.save()

            new_images = gallery_formset.save()

            if new_images:
                page.gallery_images.add(*new_images)

            return redirect('adminlte:pages')


    else:
        page_form = PageForm(instance=page)
        seo_form = SeoBlockForm(instance=seo_instance, prefix='seo')

        gallery_formset = GalleryFormSet(
            queryset=page.gallery_images.all(),
            prefix='gallery',
        )

    context = {
        'page_form': page_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
        'page': page,
    }

    return render(request, 'adminlte/page.html', context)


def page_delete(request, pk):
    page = get_object_or_404(Page, pk=pk)
    page.delete()
    return redirect('adminlte:pages')


def edit_mainpage(request):
    main_page = get_object_or_404(MainPage, pk=1)
    seo_instance = main_page.seo_block

    if request.method == 'POST':
        mainpage_form = MainPageForm(request.POST, request.FILES, instance=main_page)
        seo_form = SeoBlockForm(request.POST, instance=seo_instance, prefix='seo')

        if mainpage_form.is_valid() and seo_form.is_valid():
            seo_block = seo_form.save()
            main_page = mainpage_form.save(commit=False)
            main_page.seo_block = seo_block
            main_page.save()

            return redirect('adminlte:pages')

    else:
        mainpage_form = MainPageForm(instance=main_page)
        seo_form = SeoBlockForm(instance=seo_instance, prefix='seo')

    context = {
        'main_form': mainpage_form,
        'seo_form': seo_form,
    }


    return render(request, 'adminlte/main_page.html', context)


def contacts(request):
    contact_page = Contacts.load()
    seo_instance = contact_page.seo_block

    if request.method == 'POST':
        seo_form = SeoBlockForm(request.POST, prefix='seo', instance=seo_instance)
        formset = ContactComponentFormset(request.POST, request.FILES, queryset=contact_page.component.all())

        if seo_form.is_valid() and formset.is_valid():
            seo_block = seo_form.save()
            contact_page.seo_block = seo_block
            contact_page.save()

            instances = formset.save()

            for instance in instances:
                contact_page.component.add(instance)


            return redirect('adminlte:pages')



    else:
        seo_form = SeoBlockForm(instance=seo_instance ,prefix='seo')
        formset = ContactComponentFormset(queryset=contact_page.component.all())

    context = {
        'seo_form': seo_form,
        'formset': formset,
    }

    return render(request, 'adminlte/contacts.html', context)


def add_movie(request):

    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES)
        seo_form = SeoBlockForm(request.POST, prefix='seo')

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=Gallery.objects.none(),
            prefix='gallery',
        )

        if movie_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():
            seo_block = seo_form.save()
            movie = movie_form.save(commit=False)
            movie.seo_block = seo_block
            movie.save()

            new_images = gallery_formset.save()
            if new_images:
                movie.images.add(*new_images)

            return redirect('adminlte:film_list')

    else:
        movie_form = MovieForm()
        seo_form = SeoBlockForm(prefix='seo')
        gallery_formset = GalleryFormSet(
            queryset=Gallery.objects.none(),
            prefix='gallery'
        )


    context = {
        'movie_form': movie_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
    }

    return render(request, 'adminlte/film.html', context)


def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    seo_instance = movie.seo_block

    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES, instance=movie)

        seo_form = SeoBlockForm(request.POST, instance=seo_instance, prefix='seo')

        GalleryFormSet.extra = 0

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=movie.images.all(),
            prefix='gallery',
        )

        if movie_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():
            seo_block = seo_form.save()

            movie = movie_form.save(commit=False)

            if request.POST.get('clear_main_image') == 'true':
                movie.main_image.delete(save=False)
                movie.main_image = None

            movie.seo_block = seo_block
            movie.save()

            new_images = gallery_formset.save()

            if new_images:
                movie.images.add(*new_images)

            return redirect('adminlte:film_list')

    else:
        movie_form = MovieForm(instance=movie)
        seo_form = SeoBlockForm(instance=seo_instance, prefix='seo')

        GalleryFormSet.extra = 0

        gallery_formset = GalleryFormSet(
            queryset=movie.images.all(),
            prefix='gallery',
        )

    context = {
        'movie_form': movie_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
        'movie': movie,
    }

    return render(request, 'adminlte/film.html', context)


def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('adminlte:film_list')


def cinemas_list(request):
    cinemas = Cinema.objects.all()
    context = {
        'cinemas': cinemas,
    }
    return render(request, 'adminlte/cinemas.html', context)


def cinema_add(request):
    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, request.FILES)
        seo_form = SeoBlockForm(request.POST, prefix='seo')

        GalleryFormSet.extra = 0

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=Gallery.objects.none(),
            prefix='gallery',
        )

        if cinema_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():
            seo_block = seo_form.save()

            cinema = cinema_form.save(commit=False)
            cinema.seo_block = seo_block
            cinema.save()

            Hall.objects.create(
                id_cinema=cinema,
                number='Зал 1',
                description='Опис залу...',
                is_removable=False,
            )

            new_images = gallery_formset.save()

            if new_images:
                cinema.gallery_image.add(*new_images)

            return redirect('adminlte:cinemas_list')

    else:
        cinema_form = CinemaForm()
        seo_form = SeoBlockForm(prefix='seo')

        GalleryFormSet.extra = 0
        gallery_formset = GalleryFormSet(
            queryset=Gallery.objects.none(),
            prefix='gallery'
        )

    context = {
        'form': cinema_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
        'halls': []
    }

    return render(request, 'adminlte/cinema_add.html', context)


def edit_cinema(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    seo_instance = cinema.seo_block

    halls = Hall.objects.filter(id_cinema=cinema)

    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, request.FILES, instance=cinema)
        seo_form = SeoBlockForm(request.POST, instance=seo_instance, prefix='seo')

        GalleryFormSet.extra = 0

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=cinema.gallery_image.all(),
            prefix='gallery',
        )


        if cinema_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():
            seo_block = seo_form.save()
            cinema = cinema_form.save(commit=False)

            if request.POST.get('clear_main_image') == 'true':
                cinema.main_image.delete(save=False)
                cinema.main_image = None

            cinema.seo_block = seo_block
            cinema.save()

            new_images = gallery_formset.save()

            if new_images:
                cinema.gallery_image.add(*new_images)

            return redirect('adminlte:cinemas_list')

    else:
        cinema_form = CinemaForm(instance=cinema)
        seo_form = SeoBlockForm(instance=seo_instance, prefix='seo')

        GalleryFormSet.extra = 0

        gallery_formset = GalleryFormSet(
            queryset=cinema.gallery_image.all(),
            prefix='gallery',
        )


    context = {
        'form': cinema_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
        'halls': halls,
        'cinema': cinema
    }

    return render(request, 'adminlte/cinema_add.html', context)

def delete_cinema(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    cinema.delete()
    return redirect('adminlte:cinemas_list')



def hall_add(request, cinema_pk):

    if request.method == 'POST':

        cinema = get_object_or_404(Cinema, pk=cinema_pk)

        hall_form = HallForm(request.POST, request.FILES)
        seo_form = SeoBlockForm(request.POST, prefix='seo')

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=Gallery.objects.none(),
            prefix='gallery',
        )

        if hall_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():

            seo_block = seo_form.save()
            hall = hall_form.save(commit=False)

            if request.POST.get('clear_main_image') == 'true':
                hall.main_image.delete(save=False)
                hall.main_image = None

            hall.id_cinema = cinema
            hall.seo_block = seo_block
            hall.save()

            new_images = gallery_formset.save()

            if new_images:
                hall.gallery_image.add(*new_images)


            return redirect('adminlte:edit_cinema', pk=cinema_pk)

    else:

        hall_form = HallForm()
        seo_form = SeoBlockForm(prefix='seo')

        GalleryFormSet.extra = 0
        gallery_formset = GalleryFormSet(
            queryset=Gallery.objects.none(),
            prefix='gallery',
        )

    context = {
        'hall_form': hall_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
    }

    return render(request, 'adminlte/hall.html', context)


def hall_edit(request, cinema_pk, pk):
    hall = get_object_or_404(Hall, pk=pk)
    seo_instance = hall.seo_block

    if request.method == 'POST':
        hall_form = HallForm(request.POST, request.FILES, instance=hall)
        seo_form = SeoBlockForm(request.POST, instance=seo_instance, prefix='seo')

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=hall.gallery_image.all(),
            prefix='gallery'
        )

        if hall_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():

            hall = hall_form.save(commit=False)
            hall.seo_block = seo_form.save()
            hall.save()

            new_images = gallery_formset.save()

            if new_images:
                hall.gallery_image.add(*new_images)

            return redirect('adminlte:edit_cinema', pk=cinema_pk)


    else:
        hall_form = HallForm(instance=hall)
        seo_form = SeoBlockForm(instance=seo_instance, prefix='seo')

        GalleryFormSet.extra = 0

        gallery_formset = GalleryFormSet(
            queryset=hall.gallery_image.all(),
            prefix='gallery',
        )


    context = {
        'hall_form': hall_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
    }

    return render(request, 'adminlte/hall.html', context)


def hall_delete(request, cinema_pk, pk):
    hall = get_object_or_404(Hall, pk=pk)
    hall.delete()
    return redirect('adminlte:edit_cinema', pk=cinema_pk)



def news_and_actions(request, is_news):
    is_news_bool = bool(is_news)

    items = NewsAndActions.objects.filter(is_news=is_news_bool).order_by('-id')

    context = {
        'items': items,
        'is_news': is_news_bool,
    }

    return render(request, 'adminlte/news_and_actions.html', context)



def news_and_actions_add(request, is_news):
    if request.method == 'POST':
        news_and_actions_form = NewsAndActionsForm(request.POST, request.FILES)
        seo_form = SeoBlockForm(request.POST, prefix='seo')

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=Gallery.objects.none(),
            prefix='gallery',
        )

        if news_and_actions_form.is_valid() and gallery_formset.is_valid() and seo_form.is_valid():

            news_and_actions = news_and_actions_form.save(commit=False)
            news_and_actions.is_news = bool(is_news)
            seo_block = seo_form.save()

            news_and_actions.seo_block = seo_block
            news_and_actions.save()

            new_images = gallery_formset.save()

            if new_images:
                news_and_actions.gallery_images.add(*new_images)


            return redirect('adminlte:news_and_actions', is_news=int(is_news))

    else:

        news_and_actions_form = NewsAndActionsForm()
        seo_form = SeoBlockForm(prefix='seo')

        GalleryFormSet.extra = 0
        gallery_formset = GalleryFormSet(
            queryset=Gallery.objects.none(),
            prefix='gallery',
        )

    context = {
        'news_and_actions_form': news_and_actions_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
        'is_news': is_news,
    }

    return render(request, 'adminlte/news_and_actions_add.html', context)


def news_and_actions_edit(request, pk):
    news_and_actions = get_object_or_404(NewsAndActions, pk=pk)
    seo_instance = news_and_actions.seo_block

    if request.method == 'POST':
        news_and_actions_form = NewsAndActionsForm(request.POST, request.FILES, instance=news_and_actions)
        seo_form = SeoBlockForm(request.POST, instance=seo_instance, prefix='seo')

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=news_and_actions.gallery_images.all(),
            prefix='gallery',
        )

        if news_and_actions_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():

            seo_block = seo_form.save()

            news_and_actions = news_and_actions_form.save(commit=False)

            if request.POST.get('clear_main_image') == 'true':
                news_and_actions.main_image.delete(save=False)
                news_and_actions.main_image = None

            news_and_actions.seo_block = seo_block
            news_and_actions.save()

            new_images = gallery_formset.save()

            if new_images:
                news_and_actions.gallery_images.add(*new_images)

            return redirect('adminlte:news_and_actions', is_news=int(news_and_actions.is_news))

        else:
            print("Errors:", news_and_actions_form.errors, gallery_formset.errors)

    else:
        news_and_actions_form = NewsAndActionsForm(instance=news_and_actions)
        seo_form = SeoBlockForm(instance=seo_instance, prefix='seo')

        GalleryFormSet.extra = 0
        gallery_formset = GalleryFormSet(
            queryset=news_and_actions.gallery_images.all(),
            prefix='gallery',
        )

    context = {
        'news_and_actions_form': news_and_actions_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
        'is_news': news_and_actions.is_news,
    }

    return render(request, 'adminlte/news_and_actions_add.html', context)


def news_and_actions_delete(request, pk):
    news_and_actions = get_object_or_404(NewsAndActions, pk=pk)
    is_news = int(news_and_actions.is_news)
    news_and_actions.delete()
    return redirect('adminlte:news_and_actions', is_news=is_news)



def mailing(request):
    recent_templates = Mailing.objects.all()[:5]

    if request.method == 'POST':
        form = MailingForm(request.POST, request.FILES)

        send_to_all = request.POST.get('send_to_type') == 'all'

        if form.is_valid():
            mailing = form.save()

            if send_to_all:
                send_mass_mail_task.delay(mailing.id, user_ids=None)
                messages.success(request, "Розсилку всім користувачам розпочато!")
                return redirect('adminlte:mailing')
            else:
                return redirect('adminlte:mailing_users', mailing_id=mailing.id)
    else:
        form = MailingForm()

    context = {
        'form': form,
        'recent_templates': recent_templates,
    }
    return render(request, 'adminlte/mailing.html', context)


def mailing_users_view(request, mailing_id):
    mailing = get_object_or_404(Mailing, pk=mailing_id)
    users = User.objects.all()

    if request.method == 'POST':
        selected_users = request.POST.getlist('user_ids')

        if selected_users:
            user_ids = [int(uid) for uid in selected_users]
            send_mass_mail_task.delay(mailing.id, user_ids=user_ids)

            messages.success(request, f"Розсилку для {len(selected_users)} користувачів розпочато!")
            return redirect('adminlte:mailing')
        else:
            messages.warning(request, "Ви не обрали жодного користувача.")

    return render(request, 'adminlte/mailing_users.html', {'users': users, 'mailing': mailing})


def delete_template(request, pk):
    template = get_object_or_404(Mailing, pk=pk)
    template.delete()
    return redirect('adminlte:mailing')


def dashboard_stats(request):
    total_users = User.objects.count()

    gender_query = User.objects.values('gender').annotate(count=Count('id'))

    male_count = 0
    female_count = 0

    for item in gender_query:
        if item['gender'] == 'M':
            male_count = item['count']
        elif item['gender'] == 'F':
            female_count = item['count']

    today = timezone.now().date()
    dates = []
    sessions_data = []

    for i in range(6, -1, -1):
        check_date = today - datetime.timedelta(days=i)
        dates.append(check_date.strftime('%d.%m'))

        stat = DailyStats.objects.filter(date=check_date).first()
        sessions_data.append(stat.sessions if stat else 0)

    channels_query = User.objects.values('source').annotate(count=Count('id')).order_by('-count')

    channels_data = []
    channels_labels = []

    source_names = dict(User.SOURCE_CHOICES)

    for item in channels_query:
        key = item['source']
        label = source_names.get(key, key)
        channels_labels.append(label)
        channels_data.append(item['count'])

    map_query = User.objects.values('country').annotate(count=Count('id'))
    map_data = {item['country']: item['count'] for item in map_query if item['country']}

    context = {
        'total_users': total_users,
        'dates_json': json.dumps(dates),
        'sessions_json': json.dumps(sessions_data),
        'gender_data_json': json.dumps([male_count, female_count]),
        'channels_data_json': json.dumps(channels_data),
        'channels_labels_json': json.dumps(channels_labels),
        'map_data_json': json.dumps(map_data),
    }

    return render(request, 'adminlte/dashboard.html', context)
