import json
from datetime import date
from django.contrib.auth.models import Group
from django.http import Http404
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.serializers import CreateProjectSerializer, ProjectDetailsSerializer, UpdateProjectSerializer, \
    ProjectAssigneeSerializer
from users.models import CustomUser
from projects.models import Projects, ProjectAssignee
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# create project
class CreateProject(APIView):
    serializer_class = CreateProjectSerializer
    serializer_class2 = ProjectAssigneeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        count_project_wp = Projects.objects.filter(work_package_number=request.data['work_package_number'])
        work_package_index = request.data['work_package_number'] + '.' + str(len(count_project_wp) + 1)
        # request.data._mutable = True
        request.data['work_package_index'] = float(work_package_index)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # print(serializer.data)
            for item in request.data['assignee']:
                if serializer.data is not None:
                    temp_data = {
                        'assignee': item,
                        'is_assignee_active': 1,
                        'project': serializer.data['id']
                    }
                    serializer2 = self.serializer_class2(data=temp_data)
                    if serializer2.is_valid(raise_exception=True):
                        serializer2.save()
                        response = {
                            'success': 'True',
                            'status code': status.HTTP_200_OK,
                            'message': 'Project created successfully',
                            'data': serializer.data
                        }
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


# project details
class ProjectDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            projects_data = []
            projects = Projects.objects.filter(work_package_number=pk)
            for project in projects:
                serializer = ProjectDetailsSerializer(project)
                projects_data.append(serializer.data)
                response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'Project Details',
                            'data': projects_data}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# update project
class UpdateProject(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):
        # print(request.data)
        try:
            projects = Projects.objects.filter(work_package_index=pk)
            for project in projects:
                serializer = UpdateProjectSerializer(project, data=request.data)
                # print(serializer.is_valid())
                # print(serializer.errors)
                if serializer.is_valid():
                    print('executed')
                    serializer.save()
                    response = {
                        'success': 'True',
                        'status code': status.HTTP_200_OK,
                        'message': 'Project Updated Successful',
                        'data': serializer.data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


# pm wise project list
class PmProjectList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            projects_data = []
            projects = Projects.objects.filter(pm=pk)
            for project in projects:
                serializer = ProjectDetailsSerializer(project)
                projects_data.append(serializer.data)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'PM Project List',
                        'data': projects_data}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# assigned project list for employee
class AssignedProjectList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            projects_data = []
            assigned_projects = ProjectAssignee.objects.filter(assignee=pk).select_related('project').all()
            for project in assigned_projects:
                temp_project = Projects.objects.prefetch_related('pm').get(pk=project.id)
                serializer = ProjectDetailsSerializer(temp_project)
                projects_data.append(serializer.data)
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Assigned Project List for an employee',
                        'data': projects_data}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# assignee list of a project
class ProjectAssigneeList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            projects_data = []
            projects = Projects.objects.filter(work_package_number=pk)
            for project in projects:
                serializer = ProjectDetailsSerializer(project)
                projects_data.append(serializer.data)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'project assignee list',
                        'data': projects_data}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)

# update project
# class AddProjectAssignee(APIView):
#     permission_classes = (IsAuthenticated,)

#     def put(self, request, pk, format=None):
#         # print(request.data)
#         work_package_index = request.data.get('work_package_index')
#         assignee_id = request.data.get('assignee_id')
#         try:
#             projects = Projects.objects.filter(work_package_index=work_package_index, assignee_id=assignee_id)
#             for project in projects:
#                 serializer = UpdateProductSerializer(project, data=request.data)
#                 # print(serializer.is_valid())
#                 # print(serializer.errors)
#                 if serializer.is_valid():
#                     print('executed')
#                     serializer.save()
#                     response = {
#                         'success': 'True',
#                         'status code': status.HTTP_200_OK,
#                         'message': 'Project Updated Successful',
#                         'data': serializer.data
#                     }
#                     return Response(response, status=status.HTTP_200_OK)
#                 else:
#                     return Response(serializer.errors)
#         except Exception as e:
#             response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
#             return Response(response)


# update project
# class RemoveProjectAssignee(APIView):
#     permission_classes = (IsAuthenticated,)

#     def put(self, request, pk, format=None):
#         # print(request.data)
#         try:
#             projects = Projects.objects.filter(work_package_index=pk)
#             for project in projects:
#                 serializer = UpdateProductSerializer(project, data=request.data)
#                 # print(serializer.is_valid())
#                 # print(serializer.errors)
#                 if serializer.is_valid():
#                     serializer.save()
#                     response = {
#                         'success': 'True',
#                         'status code': status.HTTP_200_OK,
#                         'message': 'Project Updated Successful',
#                         'data': serializer.data
#                     }
#                     return Response(response, status=status.HTTP_200_OK)
#                 else:
#                     return Response(serializer.errors)
#         except Exception as e:
#             response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
#             return Response(response)
