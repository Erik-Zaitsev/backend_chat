from django.urls import path
<<<<<<< HEAD
from apps.user.views import CustomObtainAuthToken


urlpatterns = [
    path('', CustomObtainAuthToken.as_view()),
]
=======

from apps.user import views

urlpatterns = [
	path('auth/', views.ObtainAuthToken.as_view()),
	]
>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
