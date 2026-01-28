from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

]

urlpatterns += i18n_patterns(

    path('', include('src.main.urls', namespace='main')),
    path('adminlte/', include('src.core.adminlte.urls', namespace='adminlte')),
    path('user/', include('src.user.urls', namespace='user')),
    path('auth/', include('src.authentication.urls', namespace='auth')),
    path('cms/', include('src.cms.urls', namespace='cms')),
    prefix_default_language=True
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)