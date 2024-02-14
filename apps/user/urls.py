from django.urls import path
from apps.user.views import CustomObtainAuthToken


urlpatterns = [
    path('', CustomObtainAuthToken.as_view()),
]