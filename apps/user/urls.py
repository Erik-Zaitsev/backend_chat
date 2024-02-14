from django.urls import path
from apps.user.views import CustomObtainAuthToken


urlpatterns = [
    path('auth/', CustomObtainAuthToken.as_view()),
]
