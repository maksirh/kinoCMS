from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from src.cms.models import BannerComponent, ThroughBanner
from django.forms import formset_factory

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







