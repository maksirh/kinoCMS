
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('src.main.urls', namespace='main')),
    path('adminlte/', include('src.core.adminlte.urls', namespace='adminlte')),
    path('user/', include('src.user.urls', namespace='user')),
    path('auth/', include('src.authentication.urls', namespace='auth')),
]
