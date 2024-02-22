from django.urls import path
from apps.message.views import MessageGetPostAPIView, MessageDeleteAPIView, MakeIsReadMessageAPIView


urlpatterns = [
    path('<int:pk>/', MessageGetPostAPIView.as_view(), name='get_chat_or_send_message'),
    path('message/<int:pk>/', MessageDeleteAPIView.as_view(), name='delete_message_from_chat'),
    path('message/make-read/<int:pk>/', MakeIsReadMessageAPIView.as_view(), name='make_message_read'),
]