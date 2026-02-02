from ..main.models import MainPage, Page


def phone_numbers(request):
    main_page = MainPage.objects.first()

    if main_page:
        return {
            "phone1": main_page.phone_number1,
            "phone2": main_page.phone_number2,
        }

    return {
        "phone1": "",
        "phone2": "",
    }

def pages_inf(request):
    pages = Page.objects.all()
    return {
        "pages": pages,
    }

