from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from pytils.translit import slugify
from apps.user.models import CustomUser
from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey
from uuid import uuid4

class Chat(models.Model):
    '''Модель для чата.
       Чаты могут быть 2 видов:
       1. Общий чат
       2. Диалог'''
       
    CHAT_TYPE_CHOICES = (
        ('General chat', 'Общий чат'),
        ('Dialog', 'Диалог'),
    )

    name_chat = models.CharField(verbose_name='Название чата', max_length=100, default='Чат для общения')
    type_chat = models.CharField(verbose_name='Тип чата', max_length=15, 
                                 choices=CHAT_TYPE_CHOICES, default='Dialog')
    members = models.ManyToManyField(CustomUser, verbose_name='Участники')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты' 
        
    def __str__(self):
        return self.name_chat        



class File(models.Model):
    '''Модель для файла'''
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    file_name = models.CharField(
        verbose_name='Название файла',
        max_length=100
    )
    added_user = models.ForeignKey(
        CustomUser,
        verbose_name='Добавивший пользователь',
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        verbose_name='Прикреплённые файлы',
        upload_to='files/',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'txt', 'xlsx', 'pdf', 'jpg', 'png'])]
    )
    slug = models.SlugField(
        verbose_name='Ссылка',
        unique=True
    )
    date_create = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        
    def __str__(self):
        return self.slug
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.file_name)
        super().save(*args, **kwargs)



class Message(models.Model):
    '''Модель для сообщения'''
    
    chat = models.ForeignKey(
        Chat, 
        verbose_name='Чат', 
        on_delete=models.CASCADE, 
        related_name='messages'
        )
    author = ChainedForeignKey(
        CustomUser,
        chained_field='chat',
        chained_model_field='chat',
        show_all=True,
        auto_choose=True,
        sort=True,
        verbose_name='Отправитель',
        on_delete=models.CASCADE,
        related_name='messages'
        )
    text_message = models.TextField(
        verbose_name='Текст сообщения'
        )
    files = models.ManyToManyField(
        File,
        verbose_name='Прикреплённые файлы',
        blank=True
        )
    date_publication = models.DateTimeField(
        verbose_name='Дата отправки', 
        default=timezone.now
        )
    unread_users = ChainedManyToManyField(
        CustomUser,
        chained_field='chat',
        chained_model_field='chat',
        auto_choose=True,
        verbose_name='Непрочитавшие пользователи'
        )
        
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'    
    
    def __str__(self):
        return self.text_message
    
    
    
