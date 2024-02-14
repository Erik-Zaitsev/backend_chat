from rest_framework import serializers
<<<<<<< HEAD
from .models import Message, Chat
=======
from apps.message.models import Message, Chat
>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
from apps.user.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Chat
<<<<<<< HEAD
        fields = [
            'id',
            'name_chat',
            'type_chat',
            'members',
        ]
        
=======
        fields = '__all__'

>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453

class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)
    author = UserSerializer(required=False)
<<<<<<< HEAD
    
=======

>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
    class Meta:
        model = Message
        fields = [
            'id',
            'chat',
            'author',
            'text_message',
            'date_publication',
            'is_read',
        ]
        
    def create(self, validated_data):
<<<<<<< HEAD
        chat = Chat.objects.get(id=self.context['chat'])
        
        validated_data['author'] = self.context['user']
        validated_data['chat'] = chat
        
=======
        """
            Тут как видишь я получаю из объекта класса сериалайзера контекст и обращаюсь к нужному ключу, затем в словарь
            validated_data добавляю необходимые данные для того чтобы корректно создать запись в базе данных.
        """
        chat = Chat.objects.get(id=self.context['chat'])

        validated_data['author'] = self.context['user']
        validated_data['chat'] = chat
>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
        return Message.objects.create(**validated_data)
          
    