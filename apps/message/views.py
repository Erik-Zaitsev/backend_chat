from .models import Chat, Message, IsReadMessage
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
        
        latest_message = Message.objects.latest('id')
        unread_messages = [IsReadMessage(message=latest_message, user_is_read=user) for user in members if user != request.user]
        IsReadMessage.objects.bulk_create(unread_messages)
           
        return Response({'sent_message': serializer.data})



class MessageDeleteAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
               
    def delete(self, request, pk):
        '''Удаление сообщение из чата, если оно ещё не прочитано, если прочитано хотя бы одним участником- то удалять нельзя'''
        try:
            msgs = Message.objects.get(pk=pk, author=request.user).is_read_messages.all()  
        except Message.DoesNotExist:
            return Response('Message not found!', status=HTTP_404_NOT_FOUND) 
        
        for msg in msgs:
            if msg.is_read:
                return Response({'result': 'Сообщение уже прочитано! Удалить нельзя!'})

        msgs.delete()        
        return Response({'result': 'Message deleted!'})
    
 
        
# class MakeIsReadMessageAPIView(views.APIView):
#     permission_classes = (IsAuthenticated,)
    
#     def post(self, request, *args, **kwargs):
#         '''Метод берёт переданное сообщение, прочитавшего его человека и создаёт для него модель прочитанного сообщения '''
        
#         serializer = IsReadMessageSerializer(data=request.data, 
#                                              context={'user': request.user,})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'This message was read!': serializer.data})
    