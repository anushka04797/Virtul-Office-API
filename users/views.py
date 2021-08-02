from datetime import date
from django.contrib.auth.models import Group
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from users.serializers import LoginSerializer
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
                response['message'] = 'Please Check Your Email to Verify...!'
        else:
            response['message'] = 'User Not Found!'

        return Response(response, status=status_code)