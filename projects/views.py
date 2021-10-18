import datetime
import json
from datetime import date
from django.contrib.auth.models import Group
from django.http import Http404
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.serializers import CreateProjectSerializer, ProjectDetailsSerializer, UpdateProjectSerializer, \
    ProjectAssigneeSerializer, CreateTdoSerializer, CreateProjectAssigneeSerializer
from users.models import CustomUser
from projects.models import Projects, ProjectAssignee
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# create project
from users.serializers import UserDetailSerializer


class CreateProject(APIView):
    serializer_class = CreateTdoSerializer
    serializer_class2 = CreateProjectSerializer
    serializer_class3 = CreateProjectAssigneeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        count_project_wp = Projects.objects.filter(work_package_number=request.data['work_package_number'])
        work_package_index = request.data['work_package_number'] + '.' + str(len(count_project_wp) + 1)
        request.data['work_package_index'] = float(work_package_index)

        # create tdo block #####################
        tdo_data = {
            'title': request.data['task_delivery_order']
        }
        serializer_tdo = self.serializer_class(data=tdo_data)
        if serializer_tdo.is_valid(raise_exception=True):
            serializer_tdo.save()

            # create project block #####################
            request.data['task_delivery_order'] = serializer_tdo.data['id']
            serializer = self.serializer_class2(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                for item in request.data['assignee']:
                    if serializer.data is not None:

                        # create assignee block #####################
                        print('project ',serializer.data)
                        temp_data = {
                            'assignee': item,
                            'is_assignee_active': 1,
                            'project': serializer.data['id'],
                            'date_created':datetime.datetime.now(),
                            'date_updated': datetime.datetime.now()
                        }
                        serializer2 = self.serializer_class3(data=temp_data)
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
            results = []
            projects = Projects.objects.filter(work_package_number=pk)
            for project in projects:
                temp_data = {
                    "project": {},
                    "assignee": []
                }
                serializer = ProjectDetailsSerializer(project)
                temp_data["projects"] = serializer.data
                assignees = ProjectAssignee.objects.filter(project=project.id)
                for assignee in assignees:
                    assignee_serializer = ProjectAssigneeSerializer(assignee)
                    temp_data["assignee"].append(assignee_serializer.data)
                results.append(temp_data)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'Project Details',
                        'data': results}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# update project
class UpdateProject(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):
        print(request.data)
        if request.data['sub_task'] is '':
            print(request.data['sub_task'])
        else:
            print(request.data['sub_task'])
        try:
            projects = Projects.objects.filter(work_package_index=pk)
            serializer = UpdateProjectSerializer(projects, data=request.data)
            # print(serializer.is_valid())
            # print(serializer.errors)
            if serializer.is_valid():
                print('executed: ', serializer.data)
                # serializer.save()
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
            assigned_projects = ProjectAssignee.objects.filter(assignee=pk).select_related('project')
            for project in assigned_projects:
                temp_project = Projects.objects.get(pk=project.project_id)
                assignees_query_set = ProjectAssignee.objects.filter(project=temp_project.id).values()
                subtask_query_set = Projects.objects.filter(work_package_number=temp_project.work_package_number).values('sub_task','work_package_index')
                print('subtasks',subtask_query_set)
                subtasks=[]
                if len(subtask_query_set) > 0:
                    for task in subtask_query_set:
                        subtasks.append(task)
                assignees=[]
                if len(assignees_query_set) > 0 :
                    for assignee in assignees_query_set:
                        temp = CustomUser.objects.get(pk=assignee['assignee_id'])
                        #print('assignee', UserDetailSerializer(temp).data)
                        assignees.append(UserDetailSerializer(temp).data)

                serializer = ProjectDetailsSerializer(temp_project)
                #print(assignees)
                temp_data = {
                    'assignees': assignees,
                    'project': serializer.data,
                    'subtasks': subtasks
                }
                projects_data.append(temp_data)
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Assigned Project List for an employee',
                        'data': projects_data}
            return Response(response)
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
