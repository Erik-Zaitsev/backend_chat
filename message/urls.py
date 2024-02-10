from django.urls import path
from .views import MessageGetAPIView


urlpatterns = [
    path('<int:pk>/', MessageGetAPIView.as_view(), name='get_dialog'),
]