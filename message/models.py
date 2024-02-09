from django.db import models
from user.models import CustomUser
from django.utils import timezone

# Create your models here.
class Chat(models.Model):
    CHAT_TYPE_CHOICES = (
        ('General chat', 'Общий чат'),
        ('Dialog', 'Диалог'),
    )

    type_chat = models.CharField(verbose_name='Тип чата', max_length=15, 
                                 choices=CHAT_TYPE_CHOICES, default='Dialog')
    members = models.ManytoManyField(CustomUser, verbose_name='Участники')
    
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name='Чат')
    author = models.ForeignKey(CustomUser, verbose_name='Отправитель')
    text_message = models.TextField(verbose_name='Текст сообщения')
    date_publication = models.DateTimeField(verbose_name='Дата отправки', default=timezone.now)
    is_read = models.BooleanField(verbose_name='Прочитано', default=False)
        
    def __str__(self):
        return self.text_message