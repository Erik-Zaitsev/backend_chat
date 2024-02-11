from django.contrib.auth import user_logged_in
from rest_framework.authtoken.views import ObtainAuthToken

from apps.user import serializers


class ObtainAuthToken(ObtainAuthToken):
	serializer_class = serializers.AuthTokenCaseInsensitiveSerializer

	def post(self, request, *args, **kwargs):

		result = super().post(request, *args, **kwargs)
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		user = serializer.validated_data['user']
		user_logged_in.send(sender=self.__class__, request=request, user=user)
		return result