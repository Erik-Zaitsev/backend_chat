from django.urls import path
from apps.user.views import CustomObtainAuthToken, RegisterUserAPIView


urlpatterns = [
    path('auth/', CustomObtainAuthToken.as_view()),
    path('login/', RegisterUserAPIView.as_view()),
]
