from rest_framework import serializers
from .models import Message, Chat
from apps.user.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = [
            'id',
            'name_chat',
            'type_chat',
            'members',
        ]
        

class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)
    author = UserSerializer(required=False)
    unread_users = UserSerializer(many=True)
    
    class Meta:
        model = Message
        fields = [
            'id',
            'chat',
            'author',
            'text_message',
            'date_publication',
            'unread_users',
        ]
        
    def create(self, validated_data):
        chat = Chat.objects.get(id=self.context['chat'])

        validated_data['author'] = self.context['user']
        validated_data['chat'] = chat
        validated_data['unread_users'] = self.context['members']
        
        return Message.objects.create(**validated_data)
          
          
          
# class IsReadMessageSerializer(serializers.ModelSerializer):
#     message = MessageSerializer
#     users_is_read = UserSerializer(required=False, many=True)
    
#     class Meta:
#         model = IsReadMessage
#         fields = [
#             'id',
#             'chat',
#             'message',
#             'users_is_read',
#             'is_read',
#         ]
    
#     def update(self, instance, validated_data):
#         instance.chat = validated_data.get('chat', instance.chat)
#         instance.message = validated_data.get('message', instance.message)
#         instance.users_is_read = validated_data.get('users_is_read', instance.users_is_read)