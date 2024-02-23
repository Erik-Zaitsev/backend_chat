from django.db import models
from apps.user.models import CustomUser
from django.utils import timezone


class Chat(models.Model):
    '''Модель для чата.
       Чаты могут быть 2 видов:
       1. Общий чат
       2. Диалог'''
       
    CHAT_TYPE_CHOICES = (
        ('General chat', 'Общий чат'),
        ('Dialog', 'Диалог'),
    )

    name_chat = models.CharField(verbose_name='Название чата', max_length=100)
    type_chat = models.CharField(verbose_name='Тип чата', max_length=15, 
                                 choices=CHAT_TYPE_CHOICES, default='Dialog')
    members = models.ManyToManyField(CustomUser, verbose_name='Участники')
    
    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты' 
        
    def __str__(self):
        return self.name_chat        


class Message(models.Model):
    '''Модель для сообщения'''
    
    # def get_unread_users(self):
    #     print(self.chat.members)
    #     return self.chat.members
    
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(CustomUser, verbose_name='Отправитель', on_delete=models.CASCADE, related_name='messages')
    text_message = models.TextField(verbose_name='Текст сообщения')
    date_publication = models.DateTimeField(verbose_name='Дата отправки', default=timezone.now)
    unread_users = models.ManyToManyField(CustomUser, verbose_name='Непрочитавшие пользователи', related_name='unread_messages')
        
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'    
    
    def __str__(self):
        return self.text_message



# class IsReadMessage(models.Model):
#     '''Модель для прочитанных сообщений'''
    
#     chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE, related_name='chat')
#     message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE, related_name='is_read_messages')
#     users_is_read = models.ManyToManyField(CustomUser, verbose_name='Прочитавшие пользователи')
#     is_read = models.BooleanField(verbose_name='Прочитано', default=True)
    
#     class Meta:
#         verbose_name = 'Прочитанное сообщение'
#         verbose_name_plural = 'Прочитанные сообщения'
        
#     def __str__(self):
#         return self.message.text_message