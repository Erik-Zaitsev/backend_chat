from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.user.models import CustomUser


class AuthTokenCaseInsensitiveSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
        )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user_obj = get_user_model().objects.filter(email=email).first()
            
            if not user_obj:
                msg = _('There is no user with such credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            
            if not user_obj.is_active:
                msg = _('The "is_active" field at user must be set to True.')
                raise serializers.ValidationError(msg, code='authorization')           
            
            user = authenticate(request=self.context.get('request'),
                                email=user_obj.email,
                                password=password)

            if not user:
                msg = _('Incorrect password.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('The fields "email" and "password" are required.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    


class UserSerializer(serializers.ModelSerializer):
    '''Сериалайзер для того, чтобы на фронте не приходилось каждый раз запрашивать username пользователя по его id'''
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
        ]
