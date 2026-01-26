from ..main.models import MainPage, Page


def phone_numbers(request):
    main_page = MainPage.objects.first()
    return {
        "phone1": main_page.phone_number1,
        "phone2": main_page.phone_number2,
    }

def pages_inf(request):
    pages = Page.objects.all()
    return {
        "pages": pages,
    }

