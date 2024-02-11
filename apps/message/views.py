from rest_framework import views
from .models import Chat, Message
from rest_framework.response import Response
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class MessageGetPostAPIView(views.APIView):
    permission_classes = [IsAuthenticated,]
    
    '''Показ сообщений в диалоге, сортировка по дате отправки'''
    def get(self, request, *args, **kwargs):
        chat_id = kwargs.get('pk', None)
        queryset = Message.objects.filter(chat_id=chat_id).order_by('date_publication')
        return Response({'message_in_chat': MessageSerializer(queryset, many=True).data})
        
    '''Отправка сообщения в чат от пользователя, проверка на то, состоит ли отправитель в чате'''
    def post(self, request, *args, **kwargs):
        chat_id = kwargs.get('pk', None)        
        queryset = Chat.objects.get(pk=chat_id).members.all()
        # user = CustomUser.objects.get()
        print(queryset)
        print(request.data)
        # if request.data in queryset:
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Отправлено сообщение': serializer.data})
 

class MessageDeleteAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
               
    '''Удаление сообщение из чата, если оно ещё не прочитано, если прочитано - то удалять нельзя'''
    def delete(self, request, *args, **kwargs):
        message_id = kwargs.get('pk', None)
        Message.objects.get(pk=message_id).delete()
        return Response({'result': 'Сообщение удалено!'})
