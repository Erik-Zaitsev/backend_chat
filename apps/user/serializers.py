from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _
from apps.user.models import CustomUser


class AuthTokenCaseInsensitiveSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        pass


class UserSerializer(serializers.ModelSerializer):
    '''Сериалайзер для того, чтобы на фронте не приходилось каждый раз запрашивать username пользователя по его id'''
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
        ]
