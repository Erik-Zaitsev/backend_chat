from django.contrib import admin
from .models import Chat, Message


# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['type_chat',]
    
    list_filter = ['type_chat',]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'chat',
        'author',
        'text_message',
        'date_publication',
        'is_read',
    ]
    
    list_filter = ['is_read',]
    
    search_fields = ['text_message',]
    
    search_help_text = 'Поиск по полям: Текст сообщения'
    
    