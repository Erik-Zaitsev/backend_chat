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
    unread_users = UserSerializer(many=True, required=False)
    
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
        message = Message.objects.create(**validated_data)
        
        message.unread_users.add(*(i.id for i in self.context['members']))
        return message
