from django.contrib.auth import user_logged_in
from rest_framework.authtoken.views import ObtainAuthToken
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