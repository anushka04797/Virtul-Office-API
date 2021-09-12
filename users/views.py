from datetime import date, datetime
from django.contrib.auth.models import Group
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from users.serializers import ChangePasswordSerializer, LoginSerializer, RegisterSerializer, UserDetailSerializer, UserUpdateSerializer, UploadProPicSerializer
from users.models import CustomUser
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.models import User
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.core.mail import send_mail
import sms_api
import sys
from rest_framework.parsers import MultiPartParser


# user register
class Register(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, )

    def post(self, request):
        try:
            print('from views1', request.data)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print('from views2', serializer.data)
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'User registered  successfully',
                'data': []
            }
            message = "Your account has been created successfully. Please wait until your account being activated. " \
                      "you will be notified soon once it is get activated. "
            sms_api.SmsGateway.post(
                {
                'number': request.data['phone'],
                'message': message
                }
            )
            send_mail('New user registration', message, 'awronno.adhar@gmail.com', [request.data['email']], fail_silently=False,)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# user login
class Login(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        print(request.data)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            # 'exp': serializer.data['token'],
        }
        user_data = CustomUser.objects.filter(email=request.data.get('email')).first()
        status_code = status.HTTP_200_OK
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.data['group'] == request.data.get('group'):
                # if user_data.profile_pic:
                #     profilePic = '/media/'+str(user_data.profile_pic)
                # else:
                #     profilePic = str(user_data.profile_pic)
                # is_subs = ''
                # if serializer.data['group'] == 'seller':
                    # if user_data.is_subscribed == True:
                    #     subs_info = Subscription.objects.filter(seller=user_data.id).order_by('-id').first()
                    #     # print(subs_info.end_date)
                    #     if subs_info:
                    #         today = date.today()
                    #         expdate = subs_info.end_date
                    #         if today <= expdate:
                    #             is_subs = 'Yes'
                    #         else:
                    #             is_subs = 'No'
                    #     else:
                    #         is_subs = 'Never subscribe'
                response['token'] = serializer.data['token']
                response['group'] = serializer.data['group']
                # response['full_name'] = user_data.full_name
                # response['profile_pic'] = profilePic
                # response['is_subscribed'] = is_subs
                # response['is_approved'] = user_data.is_approved
                response['is_active'] = user_data.is_active
            else:
                response['success'] = 'False'
                response['status code'] = status.HTTP_400_BAD_REQUEST
                response['message'] = 'Forbidden for this user!!'
                status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)
        response['success'] = 'False'
        response['status code'] = status.HTTP_400_BAD_REQUEST
        if user_data:
            if user_data.is_active == 1:
                response['message'] = 'Please Enter Valid Credentials!'
            else:
                response['message'] = 'Please wait until your account get activated!'
        else:
            response['message'] = 'User Not Found!'
        return Response(response, status=status_code)


# user logout 
class Logout(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        # using Django logout
        logout(request)
        content = {
            'success': True,
            'status code': status.HTTP_201_CREATED,
            'message': 'logout Successfully',
        }
        return Response(content)


# user profile view
class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User found successfully',
            'data': []
        }
        try:
            user = CustomUser.objects.get(id=pk)
        except ObjectDoesNotExist:
            response['message'] = 'User not found'
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDetailSerializer(user, many=False)
        response['data'] = serializer.data
        return Response(response, status=status.HTTP_200_OK)


# user  profile update
class UserUpdate(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_class = JSONWebTokenAuthentication

    def post(self, request, pk):
        print(request.data)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Profile Updated',
            'data': []
        }
        if self.request.user.id != int(pk):
            response['status code'] = status.HTTP_400_BAD_REQUEST
            response['message'] = 'You can not update this profile!!'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=pk)
        id = user.id
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_201_CREATED)
        response['message'] = 'Something went wrong'
        response['data'] = serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# upload profile picture
class ChangeProfileImage(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request, pk):
        print(request, pk)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Profile Picture Updated',
            'data': []
        }
        if self.request.user.id != int(pk):
            response['status code'] = status.HTTP_400_BAD_REQUEST
            response['message'] = 'You can not update this profile!!'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=pk)
        serializer = UploadProPicSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_201_CREATED)
        response['message'] = 'Something went wrong'
        response['data'] = serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    model = CustomUser

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)