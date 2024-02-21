from django.contrib import admin
from .models import Chat, Message, IsReadMessage


# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['name_chat', 'type_chat',]
    
    list_filter = ['type_chat',]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'chat',
        'author',
        'text_message',
        'date_publication',
    ]
    
    search_fields = ['text_message',]
    
    search_help_text = 'Поиск по полям: Текст сообщения'
    
    
@admin.register(IsReadMessage)
class IsReadMessageAdmin(admin.ModelAdmin):
    list_display = [
        'message',
        'user_is_read',
        'is_read',
    ]
    