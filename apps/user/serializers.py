from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _


class AuthTokenCaseInsensitiveSerializer(AuthTokenSerializer):
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