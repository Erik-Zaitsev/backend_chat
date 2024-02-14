from django.urls import path
from apps.message.views import MessageGetPostAPIView, MessageDeleteAPIView


urlpatterns = [
<<<<<<< HEAD
    path('<int:pk>/', MessageGetPostAPIView.as_view(), name='get_chat_or_send_message'),
    path('message/<int:pk>/', MessageDeleteAPIView.as_view(), name='delete_message_from_chat'),
=======
	path('chat/<int:pk>/', MessageGetPostAPIView.as_view(), name='get_chat_or_send_message'),
	path('message/<int:pk>/', MessageDeleteAPIView.as_view(), name='delete_message_from_chat'),
>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
]