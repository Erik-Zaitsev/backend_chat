from django.db import models
from apps.user.models import CustomUser
from django.utils import timezone


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
    """
        Тут я добавил к полю chat related_name='messages'. Так как поле chat это по факту ссылка, то благодаря параметру
        related_name я могу теперь из модели Chat получить все сообщения, Chat.objects.get(pk=pk).messages.all(). Так
        код во вьюхе выглядит понятнее и мне нет необходимости, сначала получать из базы чат, а потом по нему искать все сообщения,
        я сделал это одним запросом
    """
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(CustomUser, verbose_name='Отправитель', on_delete=models.CASCADE)
    text_message = models.TextField(verbose_name='Текст сообщения')
    date_publication = models.DateTimeField(verbose_name='Дата отправки', default=timezone.now)
    is_read = models.BooleanField(verbose_name='Прочитано', default=False)
        
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'    
    
    def __str__(self):
        return self.author.email
