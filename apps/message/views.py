from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from django.utils.encoding import iri_to_uri
from django.utils.translation import gettext_lazy as _
from django.http.response import HttpResponse, FileResponse
from .models import Chat, Message, File
from .serializers import MessageSerializer
from .tasks import send_message_at_email
from io import BytesIO
from uuid import uuid4
from apps.user.models import CustomUser
from config.settings import FTP_HOST, FTP_USERNAME, FTP_PASSWORD, YANDEX_DISK_TOKEN
import ftplib
import yadisk
import logging



# Create your views here.
class MessageGetPostAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, pk):
        '''Показ сообщений в диалоге, сортировка по дате отправки'''
        
        try:
            messages = Chat.objects.get(pk=pk, members=request.user).messages.all().order_by('date_publication')
        except Chat.DoesNotExist:
            return Response(_('Chat not found!'), status=HTTP_404_NOT_FOUND)
        return Response({'messages_in_chat': MessageSerializer(messages, context={'request': request}, many=True).data})
        
        
    def post(self, request, pk):      
        '''Отправка сообщения в чат от пользователя, проверка на то, состоит ли отправитель в чате'''
        
        try:
            members = Chat.objects.get(pk=pk).members.all()
        except Chat.DoesNotExist:
            return Response(_('Chat not found!'), status=HTTP_404_NOT_FOUND)
        
        if request.user not in members:
            return Response(_('User has no rights!'), status=HTTP_403_FORBIDDEN)

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
            return Response(_('Message not found!'), status=HTTP_404_NOT_FOUND)
        
        for msg in unread_messages:
            msg.unread_users.remove(request.user)
            msg.save()
        
        return Response({'message': _('Message send!'), 
                         'sent_message': serializer.data})



class MessageDeleteAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
               
    def delete(self, request, pk):
        '''Удаление сообщение из чата, если оно ещё не прочитано, если прочитано хотя бы одним участником(кроме автора)
        - то удалять нельзя'''
        try:
            unread_users = Message.objects.get(pk=pk, author=request.user).unread_users.all()  
            members = Message.objects.get(pk=pk).chat.members.exclude(username=request.user)
        except Message.DoesNotExist:
            return Response(_('Message not found!'), status=HTTP_404_NOT_FOUND) 

        if members.difference(unread_users):
            return Response({'result': _("The message has already been read! You can't delete it!")})

        Message.objects.get(pk=pk).delete()     
        return Response({'result': _('Message deleted!')})
    

class MakeIsReadMessageAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def patch(self, request, pk):
        try:
            unread_members = Message.objects.get(pk=pk).unread_users.all()
            if request.user not in unread_members:
                return Response({'result': _('The messages has already been read by this user!')})
        
            message = Message.objects.get(pk=pk)
            unread_messages = Message.objects.filter(chat_id=message.chat_id, date_publication__lte=message.date_publication)
            if unread_messages:
                for msg in unread_messages:
                    msg.unread_users.remove(request.user)
                    msg.save()

        except Message.DoesNotExist:
            return Response(_('Message not found!'), status=HTTP_404_NOT_FOUND)
        
        return Response({'result': _('Messages read!')})
    
    
    
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
    
    

# class FTPServerInteraction():
#     '''
#     Класс для взаимодействия с FTP сервером
    
#     FTP_HOST, FTP_USERNAME, FTP_PASSWORD - все переменные импортированы из config.settings.py
#     значения находятся в файле .env
#     '''
#     def interaction_with_ftp_files(request, uuid):
#         file = File.objects.get(pk=uuid)
#         file_name = str(file.file_name)
#         extension_file = file_name[file_name.rfind('.'):]
#         ftp_dir = str(request.user)
        
#         # Открываю соединение с сервером
#         ftp_connect = ftplib.FTP(FTP_HOST, FTP_USERNAME, FTP_PASSWORD)
        
#         if request.method == 'GET':
#             buffer = BytesIO()
#             try:
#                 ftp_connect.cwd(ftp_dir)
#                 ftp_connect.retrbinary('retr ' + str(uuid) + extension_file, buffer.write)
#             except:
#                 response = Response({'result': _('File or directory not found!')})
#             else:
#                 response = HttpResponse(buffer.getvalue(), content_type='application/force-download')
#                 response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'' + iri_to_uri(file.file_name) + extension_file
        
        
#         elif request.method == 'POST':
#             allowed_extensions = ['.doc', '.docx', '.txt', '.xlsx', '.pdf', '.jpg', '.png']
#             if extension_file not in allowed_extensions:
#                 return Response({'result': 'Расширение файла не поддерживается! '
#                                 f'Разрешённые расширения: {allowed_extensions}'})
                
#             try:
#                 ftp_connect.cwd(ftp_dir)
#             except:
#                 ftp_connect.mkd(ftp_dir)
#                 ftp_connect.cwd(ftp_dir)

#             ftp_connect.storbinary('stor ' + str(uuid) + extension_file, request.data.get('file'))
        
#             response = Response({'result': _('File send at FTP server!')})
            
        
#         elif request.method == 'DELETE':
#             try:
#                 ftp_connect.cwd(ftp_dir)
#                 ftp_connect.delete(str(uuid) + extension_file)
#             except:
#                 response = Response({'result': _('File or directory not found!')})
#             else:
#                 response = Response({'result': _('File delete!')})
#                 file.delete()
        
        
#         # Закрываю соединение с сервером
#         ftp_connect.close()
        
#         # Возвращаю значение
#         return response
        
        

class YandexDiskInteraction():
    '''Класс для взаимодействия с Yandex Disk'ом'''
    
    def interaction_with_yandex_disk(request, uuid):
        client = yadisk.Client(token=str(YANDEX_DISK_TOKEN))
        yandex_disk_dir = '/' + str(request.user)
        file = File.objects.get(pk=uuid)
        file_name = str(file.file_name)
        extension_file = file_name[file_name.rfind('.'):]

        with client:
            if request.method == 'POST':
                allowed_extensions = ['.doc', '.docx', '.txt', '.xlsx', '.pdf', '.jpg', '.png']
                if extension_file not in allowed_extensions:
                    return Response({'result': 'Расширение файла не поддерживается! '
                                    f'Разрешённые расширения: {allowed_extensions}'})
                    
                try:
                    client.upload(request.data.get('file'), yandex_disk_dir + '/' + str(request.data.get('file')))
                except:
                    client.mkdir(yandex_disk_dir)
                    client.upload(request.data.get('file'), yandex_disk_dir + '/' + str(request.data.get('file')))
                    
                return Response({'result': _('FIle send at Yandex Disk!')})
            
            
            elif request.method == 'GET':
                buffer = BytesIO()
                try:
                    client.download(yandex_disk_dir + '/' + file_name, buffer)
                except:
                    response = Response({'result': _('File or directory not found!')})
                else:
                    response = HttpResponse(buffer.getvalue(), content_type='application/force-download')
                    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'' + iri_to_uri(file_name)
                
                
            elif request.method == 'DELETE':
                try:
                    client.remove(yandex_disk_dir + '/' + file_name, permanently=True)
                except:
                    response = Response({'result': _('File or directory not found!')})
                else:
                    response = Response({'result': _('File delete!')})
                    file.delete()
            
            
            # Возвращаем ответ
            return response
        
        
        
class GetFileAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):      
        '''Метод для отправки файла на Yandex Disk, служебная информация о файле хранится в БД'''  
        
        # Создаём запись в БД
        uuid = uuid4()
        uploaded_file = File.objects.create(
            id=uuid,
            added_user=request.user,
            file_name=str(request.data.get('file')),
        )
        
        # Отправляем файл на Yandex Disk
        return YandexDiskInteraction.interaction_with_yandex_disk(request, uuid)

    
    def get(self, request):
        '''Метод получения файла с Yandex Disk'''
        # Получаем из request uuid файла
        uuid = request.data.get('uuid')
        
        # Получение адреса электронной почты из запроса
        logger = logging.getLogger('main')
        logger.info('Файл получен!')
        us = CustomUser.objects.get(username=request.user)
        print(us.email)
        send_message_at_email.delay(us.email)
        # Получаем файл с Yandex Disk
        return YandexDiskInteraction.interaction_with_yandex_disk(request, uuid)
    
    
    def delete(self, request):
        '''Метод удаления файла с Yandex Disk'''
        # Получаем из request uuid файла
        uuid = request.data.get('uuid')
        
        # Удаляем файл с Yandex Disk
        return YandexDiskInteraction.interaction_with_yandex_disk(request, uuid)