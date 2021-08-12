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


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'date_of_birth', 'first_name', 'last_name', 'date_joined', 'phone']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'date_of_birth', 'first_name', 'last_name', 'date_joined', 'phone']

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        # instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        # instance.address = validated_data.get('address', instance.address)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)