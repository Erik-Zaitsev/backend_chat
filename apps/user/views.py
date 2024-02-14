from django.contrib.auth import user_logged_in
from rest_framework.authtoken.views import ObtainAuthToken
<<<<<<< HEAD
# from apps.user.serializers import AuthTokenCaseInsensitiveSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

# Create your views here.
class CustomObtainAuthToken(ObtainAuthToken):
    # serializer_class = AuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, 
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        })
=======

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
>>>>>>> 944a160b2fa8f031a7fa5d71894a8143aa288453
