from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
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
        return Message.objects.create(**validated_data)
          
    