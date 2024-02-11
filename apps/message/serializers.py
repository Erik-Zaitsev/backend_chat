from rest_framework import serializers
from apps.message.models import Message, Chat
from apps.user.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = '__all__'


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
            'is_read',
        ]
        
    def create(self, validated_data):
        """
            Тут как видишь я получаю из объекта класса сериалайзера контекст и обращаюсь к нужному ключу, затем в словарь
            validated_data добавляю необходимые данные для того чтобы корректно создать запись в базе данных.
        """
        chat = Chat.objects.get(id=self.context['chat'])

        validated_data['author'] = self.context['user']
        validated_data['chat'] = chat
        return Message.objects.create(**validated_data)
          
    