from django.shortcuts import render
from rest_framework import views
from .models import Chat, Message
from rest_framework.response import Response
from .serializers import MessageSerializer


# Create your views here.
class MessageGetAPIView(views.APIView):
    '''Показ сообщений в диалоге, сортировка по дате отправки'''
    def get(self, request, *args, **kwargs):
        chat_id = kwargs.get('pk', None)
        queryset = Message.objects.filter(chat_id=chat_id).order_by('date_publication')
        return Response({'message_in_chat': MessageSerializer(queryset, many=True).data})
        
    def post(self, request, *args, **kwargs):
        members = Chat.objects.get('', None)
        if request.user in members:
            serializer = MessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'Отправлено сообщение': serializer.data})
        
    def delete(self, request, *args, **kwargs):
        pass
