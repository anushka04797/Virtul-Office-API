from datetime import date

from rest_framework.serializers import Serializer
from meetings.models import Meetings
from projects.models import Projects
from django.contrib.auth.models import Group
from django.http import Http404
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from meetings.serializers import CreateMeetingsSerializer, MeetingsDetailsSerializer, MeetingsUpdateSerializer
from projects.serializers import ProjectDetailsSerializer
from users.models import CustomUser
from users.serializers import CustomUser
from evms.models import Evms
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.core.mail import send_mail
from datetime import datetime
import sms_api
import requests


# create Meeting
class CreateMeetings(APIView):
    serializer_class = CreateMeetingsSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_mail = CustomUser.objects.get(id=request.data['participant'])
            print(user_mail)
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'Meeting created successfully',
                'data': []
            }
            sms_api.SmsGateway.post({'number': "01915245171", 'message': "A meeting has been called at " + str(datetime.strptime(request.data['start_time'],"%Y-%m-%d %H:%M:%S.%f"))})
            send_mail(
                'Meeting initiated',
                'A meeting has been called at ' + str(datetime.strptime(request.data['start_time'],"%Y-%m-%d %H:%M:%S.%f")),
                'awronno.adhar@gmail.com',
                [user_mail],
                fail_silently=False,
            )
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# Meetings details
class MeetingsDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        project_data = []
        try:
            metings = Meetings.objects.get(id=pk)
            serializer = MeetingsDetailsSerializer(metings)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'Meetings Details',
                        'data': serializer.data}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# update Meetings
class UpdateMeetings(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):
        try:
            meeting = Meetings.objects.get(id=pk)
            serializer = MeetingsUpdateSerializer(meeting, data=request.data)
            if serializer.is_valid():
                serializer.save()
                user_mail = CustomUser.objects.get(id=request.data['participant'])
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'Meetings Updated Successful',
                    'data': serializer.data
                }
                send_mail(
                    'Meeting initiated',
                    'A meeting has been called at ' + str(datetime.strptime(request.data['start_time'],"%Y-%m-%d %H:%M:%S.%f")),
                    'awronno.adhar@gmail.com',
                    [user_mail],
                    fail_silently=False,
                )
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


# Meetings list
class MeetingsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        meeting_list = []
        try:
            metings = Meetings.objects.filter(participant=pk)
            for meeting in metings:
                serializer = MeetingsDetailsSerializer(meeting)
                meeting_list.append(serializer.data)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'Meetings list',
                        'data': meeting_list}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)