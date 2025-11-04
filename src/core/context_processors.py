from ..user.models import User


def user_inf(request):
    return {
        "user_inf": request.user if request.user.is_authenticated else None
    }


