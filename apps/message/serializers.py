from rest_framework import serializers
from .models import Message, Chat, File
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
        


class FileSerializer(serializers.ModelSerializer):
    # file_url = serializers.SerializerMethodField('get_file_url')
    
    # def get_file_url(self, obj):
    #     return self.context['request'].build_absolute_uri(obj.file_url)
        
    class Meta:
        model = File
        fields = [
            'id',
            'slug',
            # 'file_url'
        ]


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)
    author = UserSerializer(required=False)
    unread_users = UserSerializer(many=True, required=False)
    # files = FileSerializer(many=True, required=False)
    files = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id',
            'chat',
            'author',
            'files',
            'text_message',
            'date_publication',
            'unread_users',
        ]
        
    def get_files(self, obj):
        serializer = FileSerializer(obj, context=self.context)
        return serializer
    
    def create(self, validated_data):
        chat = Chat.objects.get(id=self.context['chat'])

        validated_data['author'] = self.context['user']
        validated_data['chat'] = chat
        message = Message.objects.create(**validated_data)
        
        message.unread_users.add(*(user.id for user in self.context['members'] if user != self.context['user']))
        return message
