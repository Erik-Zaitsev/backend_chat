<<<<<<< HEAD
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
 
=======
from rest_framework import views
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from apps.message.models import Chat, Message
from rest_framework.response import Response
from apps.message.serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated


class MessageGetPostAPIView(views.APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        """Показ сообщений в диалоге, сортировка по дате отправки"""
        messages = Chat.objects.get(pk=pk).messages.all().order_by('date_publication')
        return Response(
            {
                'messages_in_chat': MessageSerializer(messages, many=True).data
            }
        )

    def post(self, request, pk):
        """
            Отправка сообщения в чат от пользователя, проверка на то, состоит ли отправитель в чате

            Как видишь я завернул получение members в try/except, для того чтобы если будет передан неверный id чата
            вернулась нормальная ошибка. Так же теперь для того, чтобы отправить сообщение, не нужно в теле запроса передавать
            лишние данные, я все необходимое получаю из самого запроса. То есть по факту достаточно передать в теле запроса
            только text_message, автора я беру из запроса(request.user), а чат в который надо отправить из урла(pk)
        """
        try:
            members = Chat.objects.get(pk=pk).members.all()
        except Chat.DoesNotExist:
            return Response(
                'Чат не найден',
                status=HTTP_404_NOT_FOUND
            )
        if request.user not in members:
            return Response(status=HTTP_403_FORBIDDEN)
        '''
        Тут я передаю в сериалайзер контекст, а в нем необходимые данные что бы в методе create внутри сериалайзера
        получить доступ к тому что передал пользователь
        '''
        serializer = MessageSerializer(
            data=request.data,
            context={
                'user': request.user,
                'chat': pk
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
 

class MessageDeleteAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
<<<<<<< HEAD
               
    def delete(self, request, pk):
        '''Удаление сообщение из чата, если оно ещё не прочитано, если прочитано - то удалять нельзя'''

        try:
            Message.objects.get(pk=pk, is_read=False, author=request.user).delete()
        except DoesNotExist:
            return Response('Message not found!', status=HTTP_404_NOT_FOUND)
                        
        return Response({'result': 'Message deleted!'})
    
=======

    def delete(self, request, pk):
        """Удаление сообщение из чата, если оно ещё не прочитано, если прочитано - то удалять нельзя"""

        "Тут я поправил немного твою логику, я проверяю на то что в бд есть нужное сообщение и оно действительно не прочитано"
        try:
            Message.objects.get(pk=pk, is_read=False).delete()
        except Message.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(
            {
                'result': 'Сообщение удалено!'
            }
        )
>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
