from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, update_last_login
from rest_framework import serializers

from users.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    group = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        if user.is_active == 1:
            # print('yes')
            group = Group.objects.get(user=user)
            try:
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)

                update_last_login(None, user)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(
                    'User with given email and password does not exists'
                )
            return {
                'email': user.email,
                'token': jwt_token,
                'group': group,
            }
        else:
            return {
                'email': user.email,
                'token': '',
                'group': '',
            }