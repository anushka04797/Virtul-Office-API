from datetime import date
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
from evms.models import Evms
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# create Meeting
class CreateMeetings(APIView):
    serializer_class = CreateMeetingsSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Meeting created successfully',
            'data': []
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


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
            # print(serializer.is_valid())
            # print(serializer.errors)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'Meetings Updated Successful',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)