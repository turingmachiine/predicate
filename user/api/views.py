from rest_framework import views, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.api.serializers import RegistrationSerializer


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

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
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        })


class RegistrationToken(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        if request.method == 'POST':
            serializer = RegistrationSerializer(data=request.data)
            response_data = {}
            if serializer.is_valid():
                user = serializer.save()
                response_data['response'] = 'Successfully created account'
                response_data['username'] = user.username
                response_data['email'] = user.email
                response_data['first_name'] = user.first_name
                response_data['last_name'] = user.last_name
                response_data['token'] = Token.objects.get(user=user).key
            else:
                response_data = serializer.errors
            return Response(response_data)
