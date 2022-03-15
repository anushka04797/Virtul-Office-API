import itertools

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from projects.models import Projects
from projects.serializers import SubTaskSerializer
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
            users = UserDetailSerializer(
                CustomUser.objects.filter(Q(first_name__icontains=key) | Q(last_name__icontains=key)), many=True).data
            projects = SubTaskSerializer(
                Projects.objects.filter(Q(sub_task__icontains=key) | Q(task_title__icontains=key)), many=True).data
            result = itertools.chain(users, projects)
            for user in users:
                user['type'] = CustomUser.__name__

            for project in projects:
                project['type'] = Projects.__name__

            # for chain in result:
            #     chain = {
            #         # 'name': (b, a) [chain['type'] ==  < b]
            #     }

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
