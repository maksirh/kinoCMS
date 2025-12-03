from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from src.cms.models import BannerComponent, ThroughBanner
from django.forms import formset_factory
from src.user.models import User
from django.contrib.auth import get_user_model
from src.authentication.forms import UserUpdateForm
from django.core.paginator import Paginator
from django.db.models import Q


def index(request):
    return render(request, 'adminlte/dashboard.html')


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

def films(request):
    return render(request, 'adminlte/films.html')


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


def about_cinema(request):
    page, created = Page.objects.get_or_create(id=1)

    if not page.seo_block:
        page.seo_block = SeoBlock.objects.create()
        page.save()

    if request.method == 'POST':
        page_form = PageForm(request.POST, request.FILES, instance=page)
        seo_form = SeoBlockForm(request.POST, instance=page.seo_block)

        gallery_formset = GalleryFormSet(
            request.POST,
            request.FILES,
            queryset=page.gallery_images.all(),
            prefix='gallery'
        )

        if page_form.is_valid() and seo_form.is_valid() and gallery_formset.is_valid():
            page_obj = page_form.save()
            seo_form.save()

            gallery_images = gallery_formset.save()

            for new_image in gallery_images:
                page_obj.gallery_images.add(new_image)

            for deleted_image in gallery_formset.deleted_objects:
                page_obj.gallery_images.remove(deleted_image)

            return redirect('adminlte:about_cinema')

    else:
        page_form = PageForm(instance=page)
        seo_form = SeoBlockForm(instance=page.seo_block)
        gallery_formset = GalleryFormSet(queryset=page.gallery_images.all(), prefix='gallery')

    context = {
        'page_form': page_form,
        'seo_form': seo_form,
        'gallery_formset': gallery_formset,
        'page': page,
    }
    return render(request, 'adminlte/about_cinema.html', context)


