from django.contrib import admin
from django.urls import path, include, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/chat/', include('apps.message.urls')),
    path('api-token-auth/', include('apps.user.urls')),
    path('register/', include('apps.user.urls')),

]
