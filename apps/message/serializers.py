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
    added_user = UserSerializer(required=False)
    # file_url = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    
    # def get_file_url(self, obj):
    #     request = self.context['request']
    #     return request.build_absolute_uri(obj.file.url)
        
    def get_link(self, obj):
        return 'http://127.0.0.1:8000/api/v1/file/' + str(obj.pk) 
        
    class Meta:
        model = File
        fields = [
            'id',
            'file_name',
            # 'file_url',
            'added_user',
            'link'
        ]


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)
    author = UserSerializer(required=False)
    unread_users = UserSerializer(many=True, required=False)
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
        return FileSerializer(obj.files.all(), 
                              context={'request': self.context['request']}, 
                              many=True, required=False).data
    
    def create(self, validated_data):
        chat = Chat.objects.get(id=self.context['chat'])

        validated_data['author'] = self.context['user']
        validated_data['chat'] = chat
        message = Message.objects.create(**validated_data)
        
        message.unread_users.add(*(user.id for user in self.context['members'] if user != self.context['user']))
        return message
