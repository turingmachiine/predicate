from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_subscriber', 'queries']


class RegistrationSerializer(serializers.ModelSerializer):

    confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password, confirm = self.validated_data['password'], self.validated_data['confirm']
        if password != confirm:
            raise ValidationError({'password': 'Пароли должны совпадать'})
        user.set_password(password)
        user.save()
        return user
