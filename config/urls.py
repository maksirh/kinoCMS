
from django.contrib import admin
from django.urls import path, include
# from src.core.adminlte.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('src.main.urls', namespace='main')),
    path('adminlte/', include('src.core.adminlte.urls', namespace='adminlte')),
]
