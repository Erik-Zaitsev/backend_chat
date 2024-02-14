from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _
<<<<<<< HEAD
=======

>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
from apps.user.models import CustomUser


class AuthTokenCaseInsensitiveSerializer(AuthTokenSerializer):
<<<<<<< HEAD
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
=======
	def validate(self, attrs):
		username = attrs.get('username')
		password = attrs.get('password')

		if username and password:
			user_obj = get_user_model().objects.filter(email__iexact=username).first()

			if not user_obj:
				msg = _('Unable to log in with provided credentials.')
				raise serializers.ValidationError(msg, code='authorization')

			user = authenticate(
				request=self.context.get('request'),
				username=user_obj.get_username(),
				password=password
			)

			if not user:
				msg = _('Unable to log in with provided credentials.')
				raise serializers.ValidationError(msg, code='authorization')
		else:
			msg = _('Must include "username" and "password".')
			raise serializers.ValidationError(msg, code='authorization')

		attrs['user'] = user
		return attrs


class UserSerializer(serializers.ModelSerializer):
	"""
		Этот сериазайзер нужен для того чтобы на фронте не приходилось каждый раз запрашивать username пользователя
		по его id. Я его переиспользую в других сериалайзерах, и он автоматом подставляет там нужные поля
	"""
	class Meta:
		model = CustomUser
		fields = [
			'id',
			'username'
		]
>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
