from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import AuthTokenCaseInsensitiveSerializer, RegisterUserSerializer
from rest_framework import views


# Create your views here.
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenCaseInsensitiveSerializer
    
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



class RegisterUserAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({'Пользователь был добавлен': serializer.data})