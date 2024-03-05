from .models import Chat, Message, File
from .serializers import MessageSerializer
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from django.utils.encoding import iri_to_uri
from django.http.response import HttpResponse
from config.settings import ftp_host, ftp_username, ftp_password
import ftplib
from io import BytesIO


# Create your views here.
class MessageGetPostAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, pk):
        '''Показ сообщений в диалоге, сортировка по дате отправки'''
        
        try:
            messages = Chat.objects.get(pk=pk, members=request.user).messages.all().order_by('date_publication')
        except Chat.DoesNotExist:
            return Response('Chat not found!', status=HTTP_404_NOT_FOUND)
        return Response({'message_in_chat': MessageSerializer(messages, context={'request': request}, many=True).data})
        
        
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
                                            'chat': pk,
                                            'members': members,
                                            'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # После отправки сообщения в чат - все предыдущие сообщения становятся прочитанными
        try:
            unread_messages = Chat.objects.get(pk=pk).messages.filter(unread_users=request.user)
        except Chat.DoesNotExist:
            return Response('Message not found!', status=HTTP_404_NOT_FOUND)
        
        for msg in unread_messages:
            msg.unread_users.remove(request.user)
            msg.save()
        
        return Response({'sent_message': serializer.data})



class MessageDeleteAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
               
    def delete(self, request, pk):
        '''Удаление сообщение из чата, если оно ещё не прочитано, если прочитано хотя бы одним участником(кроме автора)
        - то удалять нельзя'''
        try:
            unread_users = Message.objects.get(pk=pk, author=request.user).unread_users.all()  
            members = Message.objects.get(pk=pk).chat.members.exclude(username=request.user)
        except Message.DoesNotExist:
            return Response('Message not found!', status=HTTP_404_NOT_FOUND) 

        if members.difference(unread_users):
            return Response({'result': 'Сообщение уже прочитано! Удалить нельзя!'})

        Message.objects.get(pk=pk).delete()     
        return Response({'result': 'Message deleted!'})
    

class MakeIsReadMessageAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def patch(self, request, pk):
        try:
            unread_members = Message.objects.get(pk=pk).unread_users.all()
            if request.user not in unread_members:
                return Response({'result': 'Сообщения уже прочитаны этим пользователем!'})
        
            message = Message.objects.get(pk=pk)
            unread_messages = Message.objects.filter(chat_id=message.chat_id, date_publication__lte=message.date_publication)
            if unread_messages:
                for msg in unread_messages:
                    msg.unread_users.remove(request.user)
                    msg.save()

        except Message.DoesNotExist:
            return Response('Message not found!', status=HTTP_404_NOT_FOUND)
        
        return Response({'result': 'Сообщения прочитаны!'})
    
    
    
class GetAllUnReadMessages(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        chats = Chat.objects.filter(members=request.user)
        count_messages = 0
        
        if chats:
            for chat in chats:
                sms = chat.messages.filter(unread_users=request.user).exclude(author=request.user)
                count_messages += len(sms)
        else:
            return Response({'result': (f'Пользователь {request.user} не состоит в чатах!')})
        
        return Response({'result': (f'У пользователя {request.user} {count_messages} непрочитанных сообщений в {len(chats)} чатах')})
    
    

class FTPServerInteraction():
    '''
    Класс для взаимодействия с FTP сервером
    
    ftp_host, ftp_username, ftp_password - все переменные импортированы из config.settings.py
    значения находятся в файле .env
    '''
    def interaction_with_ftp_files(request, uuid):
        file = File.objects.get(pk=uuid)
        string = str(file.file)
        excpansion_file = string[string.rfind('.'):]
        ftp_dir = str(request.user)
        
        # Открываю соединение с сервером
        ftp_connect = ftplib.FTP(ftp_host, ftp_username, ftp_password)
        
        if request.method == 'GET':
            buffer = BytesIO()
            try:
                ftp_connect.cwd(ftp_dir)
                ftp_connect.retrbinary('retr ' + uuid + excpansion_file, buffer.write)
            except:
                response = Response({'result':'File or directory not found!'})
            else:
                response = HttpResponse(buffer.getvalue(), content_type='application/force-download')
                response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'' + iri_to_uri(file.file_name) + excpansion_file
        
        
        elif request.method == 'POST':
            try:
                ftp_connect.cwd(ftp_dir)
            except:
                ftp_connect.mkd(ftp_dir)
                ftp_connect.cwd(ftp_dir)

            with open('media/' + string, 'rb') as fp:
                ftp_connect.storbinary('stor ' + uuid + excpansion_file, fp)
        
            response = Response({'result': 'File send!'})
            
        
        elif request.method == 'DELETE':
            try:
                ftp_connect.cwd(ftp_dir)
                ftp_connect.delete(uuid + excpansion_file)
            except:
                response = Response({'result': 'File or directory not found!'})
            else:
                response = Response({'result': 'File delete!'})
        
        
        # Закрываю соединение с сервером
        ftp_connect.close()
        
        # Возвращаем значение
        return response
        
        

class GetFileAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, uuid):
        return FTPServerInteraction.interaction_with_ftp_files(request, uuid)
        # file = File.objects.get(pk=uuid)
        # string = str(file.file)
        # excpansion_file = string[string.rfind('.'):]
        # ftp_connect = ftplib.FTP(ftp_host, ftp_username, ftp_password)
        # ftp_dir = str(request.user)
        
        # try:
        #     ftp_connect.cwd(ftp_dir)
        # except:
        #     ftp_connect.mkd(ftp_dir)
        #     ftp_connect.cwd(ftp_dir)
            
        # with open('media/' + str(file.file), 'rb') as fp:
        #     ftp_connect.storbinary('stor ' + uuid + excpansion_file, fp)
        # ftp_connect.close()
        
        # return Response({'result': 'File send!'})
    
    
    def get(self, request, uuid):
        return FTPServerInteraction.interaction_with_ftp_files(request, uuid)
        # file = File.objects.get(pk=uuid)
        # string = str(file.file)
        # excpansion_file = string[string.rfind('.'):]
        # ftp_connect = ftplib.FTP(ftp_host, ftp_username, ftp_password)
        # ftp_dir = str(request.user)
        # buffer = BytesIO()
        
        # try:
        #     ftp_connect.cwd(ftp_dir)
        #     response = ftp_connect.retrbinary('retr ' + uuid + excpansion_file, buffer.write)
        #     ftp_connect.close()
        # except:
        #     return Response({'result':'File or directory not found!'})
        # response = HttpResponse(buffer.getvalue(), content_type='application/force-download')
        # response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'' + iri_to_uri(file.file_name) + excpansion_file
        # return response
    
    
    def delete(self, request, uuid):
        return FTPServerInteraction.interaction_with_ftp_files(request, uuid)
        # ftp_connect = ftplib.FTP(ftp_host, ftp_username, ftp_password)
        # ftp_dir = str(request.user)
        
        # try:
        #     ftp_connect.cwd(ftp_dir)
        #     ftp_connect.delete(uuid)
        # except:
        #     return Response({'result': 'File or directory not found!'})
        
        # ftp_connect.close()
        # return Response({'result': 'File delete!'})