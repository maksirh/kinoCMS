from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.main.urls', namespace='main')),
    path('adminlte/', include('src.core.adminlte.urls', namespace='adminlte')),
    path('user/', include('src.user.urls', namespace='user')),
    path('auth/', include('src.authentication.urls', namespace='auth')),
    path('cms/', include('src.cms.urls', namespace='cms')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)