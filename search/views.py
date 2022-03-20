import itertools

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from meetings.models import Meetings
from meetings.serializers import MeetingsDetailsSerializer
from projects.models import Projects
from projects.serializers import ProjectDetailsSerializer
from users.models import CustomUser
from users.serializers import UserDetailSerializer


class Search(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        try:
            models = {
                'user': 'CustomUser',
                'project': 'Projects'
            }
            key = request.GET.get('key')
            users = UserDetailSerializer(CustomUser.objects.filter(Q(first_name__icontains=key) | Q(last_name__icontains=key)), many=True).data
            projects = ProjectDetailsSerializer(Projects.objects.filter(Q(sub_task__icontains=key) | Q(task_title__icontains=key)), many=True).data
            #meetings = MeetingsDetailsSerializer(Meetings.objects.filter(Q(sub_task__icontains=key) | Q(task_title__icontains=key)), many=True).data
            result = {
                'employees':users,
                'projects':projects
            }

            response = {
                'success': True,
                'status code': status.HTTP_200_OK,
                'data': result
            }
            # return Response(response)
        except Exception as e:
            print("line 52")
            response = {
                'success': 'False',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
            }
            print(str(e))

        return Response(response)
