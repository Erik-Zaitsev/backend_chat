from .models import Chat, Message
from .serializers import MessageSerializer
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND


# Create your views here.
class MessageGetPostAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, pk):
        '''Показ сообщений в диалоге, сортировка по дате отправки'''
        
        try:
            messages = Chat.objects.get(pk=pk, members=request.user).messages.all().order_by('date_publication')
        except Chat.DoesNotExist:
            return Response('Chat not found!', status=HTTP_404_NOT_FOUND)
        return Response({'message_in_chat': MessageSerializer(messages, many=True).data})
        
        
    def post(self, request, pk):      
        '''Отправка сообщения в чат от пользователя, проверка на то, состоит ли отправитель в чате'''
        
        try:
            members = Chat.objects.get(pk=pk).members.all()
        except Chat.DoesNotExist:
            return Response('Chat not found!', status=HTTP_404_NOT_FOUND)
        
        if request.user not in members:
            return Response('У пользователя недостаточно прав!', status=HTTP_403_FORBIDDEN)
        
        serializer = MessageSerializer(data=request.data, 
                                       context={
                                            'user': request.user, 
                                            'chat': pk})
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'sent_message': serializer.data})



class MessageDeleteAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
               
    def delete(self, request, pk):
        '''Удаление сообщение из чата, если оно ещё не прочитано, если прочитано - то удалять нельзя'''

        try:
            Message.objects.get(pk=pk, is_read=False, author=request.user).delete()
        except DoesNotExist:
            return Response('Message not found!', status=HTTP_404_NOT_FOUND)
                        
        return Response({'result': 'Message deleted!'})
    

    
class MakeMessageReadAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def patch(self, request, pk):
        '''Метод редактирует поле "is_read" указанного сообщения'''
        
        try:
            Chat.objects.get(pk=pk).messages.all().update(is_read=True)
        except:
            return Response('Messages not found', status=HTTP_404_NOT_FOUND)

        return Response({'result', 'Messages in this chat was read!'})
            