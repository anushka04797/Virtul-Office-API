import datetime
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.serializers import SubTaskSerializer, CreateProjectSerializer, ProjectDetailsSerializer, \
    UpdateProjectSerializer, ProjectAssigneeSerializer, TdoSerializer, CreateProjectAssigneeSerializer, \
    UpdateSubTaskSerializer, TaskSerializer
from users.models import CustomUser
from projects.models import Projects, ProjectAssignee, Tdo
from rest_framework.permissions import IsAuthenticated, AllowAny


# create project
from users.serializers import UserDetailSerializer


class CreateProject(APIView):
    serializer_class = TdoSerializer
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
                        print('project ', serializer.data)
                        temp_data = {
                            'assignee': item,
                            'is_assignee_active': 1,
                            'project': serializer.data['id'],
                            'date_created': datetime.datetime.now(),
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

#new project details
class NewProjectDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, pk):
        try:
            projects = Projects.objects.filter(work_package_number=pk)
            subtask = SubTaskSerializer(projects[0]).data
            tasks = TaskSerializer(projects, many=True).data
            response_data = {
                #"tdo": subtask["task_delivery_order"],
                "project": subtask,
                "tasks": tasks,
                "assignees": []
            }
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'Project Details',
                        'data': response_data}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)



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
        try:
            projects = Projects.objects.get(work_package_index=pk)
            serializer = UpdateProjectSerializer(projects, data=request.data)
            if serializer.is_valid():
                serializer.save()
                assignees = request.data['assignee']
                for assignee in assignees:
                    if not ProjectAssignee.objects.filter(assignee=assignee, project=serializer.data['id']).exists():
                        temp_data = {
                            'assignee': assignee,
                            'is_assignee_active': 1,
                            'project': serializer.data['id'],
                            'date_created': datetime.datetime.now(),
                            'date_updated': datetime.datetime.now()
                        }
                        serializer2 = CreateProjectAssigneeSerializer(data=temp_data)
                        if serializer2.is_valid(raise_exception=True):
                            serializer2.save()
                if request.data['sub_task_updated']:
                    work_package_number = pk.split('.')[0]
                    sub_task_to_update = Projects.objects.filter(work_package_number=work_package_number)
                    for sub_task in sub_task_to_update:
                        serializer3 = UpdateSubTaskSerializer(sub_task, request.data)
                        if serializer3.is_valid():
                            serializer3.save()
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
            projects = Projects.objects.filter(pm=pk)
            serializer = ProjectDetailsSerializer(projects, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'PM Project List',
                        'data': serializer.data}
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
                subtask_query_set = Projects.objects.filter(work_package_number=temp_project.work_package_number)
                #print('subtasks',subtask_query_set)
                subtasks=[]
                if len(subtask_query_set) > 0:
                    for task in subtask_query_set:
                        serialized_task = ProjectDetailsSerializer(task)
                        subtasks.append(serialized_task.data)
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
            projects = Projects.objects.filter(work_package_number=pk)
            serializer = ProjectDetailsSerializer(projects, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'project assignee list',
                        'data': serializer.data}
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


class DeleteSubTask(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self,request,work_package_index):
        try:
            Projects.objects.filter(work_package_index=work_package_index).delete()
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Sub Task has been deleted'}
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


class ChangeTDOTitle(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        try:
            tdo = Tdo.objects.get(pk=pk)
            tdo.title = request.data['title']
            tdo.save()
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Task Delivery order name has been changed'}
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


class TdoList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):

        try:
            tdo_list = Tdo.objects.all()
            serialized_data = TdoSerializer(tdo_list, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'data': serialized_data.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)