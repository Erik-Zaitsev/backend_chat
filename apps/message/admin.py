from django.contrib import admin
from .models import Chat, Message


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
    
    
# @admin.register(IsReadMessage)
# class IsReadMessageAdmin(admin.ModelAdmin):
#     list_display = [
#         'message',
#         # 'users_is_read',
#         'is_read',
#     ]
    
    # def get_queryset(self, request):
    #     """
    #     Return a QuerySet of all model instances that can be edited by the
    #     admin site. This is used by changelist_view.
    #     """
    #     # qs = self.model._default_manager.get_queryset()
    #     # # TODO: this should be handled by some parameter to the ChangeList.
    #     # ordering = self.get_ordering(request)
    #     # if ordering:
    #     #     qs = qs.order_by(*ordering)
    #     # return qs
    
    #     # queryset = super().get_queryset(request)
    #     # queryset = queryset.prefetch_related('members')
    #     # return queryset 
    #     return Chat.members