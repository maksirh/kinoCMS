from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from src.cms.models import BannerComponent
from django.forms import formset_factory

def index(request):
    return render(request, 'adminlte/dashboard.html')


def banners_and_sliders(request, banner_id=None):
    banner = Banner.objects.order_by('pk').first()
    if banner is None:
        banner = Banner.objects.create(speed=5, is_active=True, is_promo=False)

    if request.method == "POST":
        form = BannerForm(request.POST, instance=banner)
        formset = BannerComponentFormSet(
            request.POST, request.FILES,
            queryset=banner.banner_component.all(),
            prefix="items"
        )

        if form.is_valid() and formset.is_valid():
            banner = form.save()

            for f in formset.deleted_forms:
                obj = f.instance
                if obj.pk:
                    banner.banner_component.remove(obj)
                    obj.delete()

            components = formset.save(commit=False)

            instances = formset.save(commit=False)
            for obj in instances:
                obj.save()
                banner.banner_component.add(obj)

        return redirect("adminlte:banners")

    form = BannerForm(instance=banner)
    formset = BannerComponentFormSet(
        queryset=banner.banner_component.all(),
        prefix='items',
    )

    return render(request, "adminlte/banners_edit.html", {
        "form": form,
        "formset": formset,
    })





def films(request):
    return render(request, 'adminlte/films.html')







