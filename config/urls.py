from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/chat/', include('apps.message.urls')),
    # path('api/v1/auth/', include('apps.user.urls')),
    path('api-token-auth/', include('apps.user.urls')),
    # path('api-token-auth/', views.obtain_auth_token)
]
