from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.message.urls')),
    path('api-token-auth/', include('apps.user.urls')),
    path('register/', include('apps.user.urls')),
    re_path(r'^chaining/', include('smart_selects.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)