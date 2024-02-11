from django.db import models
from user.models import CustomUser
from django.utils import timezone

# Create your models here.
class Chat(models.Model):
    CHAT_TYPE_CHOICES = (
        ('General chat', 'Общий чат'),
        ('Dialog', 'Диалог'),
    )

    name_chat = models.CharField(verbose_name='Название чата', max_length=100, default='ewrr')
    type_chat = models.CharField(verbose_name='Тип чата', max_length=15, 
                                 choices=CHAT_TYPE_CHOICES, default='Dialog')
    members = models.ManyToManyField(CustomUser, verbose_name='Участники')
    
    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты' 
        
    def __str__(self):
        return self.name_chat        
    


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, verbose_name='Отправитель', on_delete=models.CASCADE)
    text_message = models.TextField(verbose_name='Текст сообщения')
    date_publication = models.DateTimeField(verbose_name='Дата отправки', default=timezone.now)
    is_read = models.BooleanField(verbose_name='Прочитано', default=False)
        
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'    
    
    def __str__(self):
        return self.text_message