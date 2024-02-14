from django.contrib import admin
<<<<<<< HEAD:config/urls.py
from django.urls import path, include, re_path
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/chat/', include('apps.message.urls')),
    # path('api/v1/auth/', include('apps.user.urls')),
    path('api-token-auth/', include('apps.user.urls')),
    # path('api-token-auth/', views.obtain_auth_token)
=======
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.user.urls')),
    path('api/v1/', include('apps.message.urls')),
>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453:chat/urls.py
]
