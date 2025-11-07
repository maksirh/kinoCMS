from django.urls import path
from .views import login_user, register, profile, logout_user
from django.conf.urls.static import static
from django.conf import settings

app_name = 'authentication'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_user, name='logout'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)