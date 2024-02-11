from django.urls import path

from apps.user import views

urlpatterns = [
	path('auth/', views.ObtainAuthToken.as_view()),
	]