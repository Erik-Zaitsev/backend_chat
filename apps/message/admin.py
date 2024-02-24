from django.contrib import admin
from .models import Chat, Message


# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = [
        'name_chat', 
        'type_chat', 
        'get_members',
        ]
    
    list_filter = ['type_chat',]
    
    @admin.display(description='Участники чата')
    def get_members(self, obj):
        return ',\n'.join([user.username for user in obj.members.all()])


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'chat',
        'author',
        'text_message',
        'date_publication',
        'get_unread_users',
    ]
    
    @admin.display(description='Непрочитавшие пользователи')
    def get_unread_users(self, obj):
        return ',\n'.join([user.username for user in obj.unread_users.all()])
    
    search_fields = ['text_message',]
    
    search_help_text = 'Поиск по полям: Текст сообщения'
    