from rest_framework import serializers
from .models import Message, Chat, IsReadMessage
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
    
    class Meta:
        model = Message
        fields = [
            'id',
            'chat',
            'author',
            'text_message',
            'date_publication',
        ]
        
    def create(self, validated_data):
        chat = Chat.objects.get(id=self.context['chat'])
        
        validated_data['author'] = self.context['user']
        validated_data['chat'] = chat
        
        return Message.objects.create(**validated_data)
          
          
          
# class IsReadMessageSerializer(serializers.ModelSerializer):
#     message = MessageSerializer
#     user_is_read = UserSerializer(required=False)
    
#     class Meta:
#         model = IsReadMessage
#         fields = [
#             'id',
#             'message',
#             'user_is_read',
#             'is_read',
#         ]
    
#     def create(self, validated_data):
#         validated_data['message'] = request.data.message
#         validated_data['user_is_read'] = self.context['user']
#         validated_data['is_read'] = True
        
#         return IsReadMessage.objects.create(**validated_data)