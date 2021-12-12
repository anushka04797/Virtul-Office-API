import datetime
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from projects.serializers import SubTaskSerializer, CreateProjectSerializer, ProjectDetailsSerializer, \
    UpdateProjectSerializer, ProjectAssigneeSerializer, TdoSerializer, CreateProjectAssigneeSerializer, \
    UpdateSubTaskSerializer, TaskSerializer, ProjectFileSerializer, DocumentListSerializer
from users.models import CustomUser
from projects.models import Projects, ProjectAssignee, Tdo, ProjectSharedFiles
from rest_framework.permissions import IsAuthenticated, AllowAny


# create project
from users.serializers import UserDetailSerializer


class CreateProject(APIView):
    serializer_class = TdoSerializer
    serializer_class2 = CreateProjectSerializer
    serializer_class3 = CreateProjectAssigneeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data)
        count_project_wp = Projects.objects.filter(work_package_number=request.data['work_package_number'])
        work_package_index = request.data['work_package_number'] + '.' + str(len(count_project_wp) + 1)
        request.data['work_package_index'] = float(work_package_index)

        if not Tdo.objects.filter(title=request.data['task_delivery_order']).exists():
            # create tdo block #####################
            tdo_data = {
                'title': request.data['task_delivery_order'],
                'description': request.data['tdo_details']
            }
            serializer_tdo = self.serializer_class(data=tdo_data)
            if serializer_tdo.is_valid(raise_exception=True):
                serializer_tdo.save()
                request.data['task_delivery_order'] = serializer_tdo.data['id']
        else:
            request.data['task_delivery_order'] = TdoSerializer(Tdo.objects.filter(title=request.data['task_delivery_order'])[0]).data['id']

        if request.data['task_delivery_order'] is not None:
            # create project block #####################
            # request.data['date_created'] = datetime.datetime.now()
            # request.data['date_updated'] = datetime.datetime.now()
            serializer = self.serializer_class2(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                count = 0
                for item in request.data['assignee']:
                    print(request.data['estimated_person'][0])
                    if serializer.data is not None:

                        # create assignee block #####################
                        print('project ', serializer.data)
                        temp_data = {
                            'assignee': item,
                            'estimated_person': request.data['estimated_person'][count],
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
                    count = count + 1
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

#new project details


def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list


class NewProjectDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, pk):
        try:
            projects = Projects.objects.filter(work_package_number=pk)
            serialized_subtask=''
            if len(projects)>0:
                serialized_subtask = SubTaskSerializer(projects[0]).data
            tasks = TaskSerializer(projects, many=True).data
            assignees=[]
            for task in tasks:
                # temp_assignees= ProjectAssignee.objects.filter(project_id=task['id'])
                task_assignees = ProjectAssigneeSerializer(ProjectAssignee.objects.filter(project_id=task['id']),many=True).data
                task['assignees']=task_assignees
                for task_assignee in task_assignees:
                    assignees.append(UserDetailSerializer(task_assignee['assignee']).data)

            assignees=unique(assignees)
            response_data = {
                #"tdo": subtask["task_delivery_order"],
                "project": serialized_subtask,
                "subtasks": tasks,
                "assignees": assignees
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
        return Response(response,status=status.HTTP_404_NOT_FOUND)


# update project
class UpdateProject(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):
        try:
            # print(request.data)
            projects = Projects.objects.get(work_package_index=pk)
            serializer = UpdateProjectSerializer(projects, data=request.data)

            if serializer.is_valid():
                serializer.save()
                count = 0
                assignees = request.data['assignee']
                for assignee in assignees:
                    if not ProjectAssignee.objects.filter(assignee=assignee, project=serializer.data['id']).exists():
                        temp_data = {
                            'assignee': assignee,
                            'estimated_person': request.data['estimated_person'][count],
                            'is_assignee_active': 1,
                            'project': serializer.data['id'],
                            'date_created': datetime.datetime.now(),
                            'date_updated': datetime.datetime.now()
                        }
                        serializer2 = CreateProjectAssigneeSerializer(data=temp_data)
                        if serializer2.is_valid(raise_exception=True):
                            serializer2.save()
                    count = count + 1
                all_assignees= ProjectAssigneeSerializer(ProjectAssignee.objects.filter(project=serializer.data['id']), many=True).data
                for assignee in all_assignees:
                    if int(assignee['assignee']['id']) not in assignees:
                        ProjectAssignee.objects.filter(assignee=assignee['assignee']['id'],project=serializer.data['id']).delete()
                # if request.data['sub_task_updated']:
                work_package_number = pk.split('.')[0]
                Projects.objects.filter(work_package_number=work_package_number).update(sub_task=request.data['sub_task'])
                # sub_task_to_update = Projects.objects.filter(work_package_number=work_package_number)
                # for sub_task in sub_task_to_update:
                #     serializer3 = UpdateSubTaskSerializer(sub_task, request.data)
                #     if serializer3.is_valid():
                #         serializer3.save()
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


class PmProjectAllAssigneeList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            tasks = Projects.objects.filter(pm=pk)
            assignees = []
            for task in tasks:
                temp_assignees = ProjectAssigneeSerializer(ProjectAssignee.objects.filter(project=task.id),
                                                           many=True).data
                for item in temp_assignees:
                    assignees.append(UserDetailSerializer(item['assignee']).data)
            assignees = unique(assignees)
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'My Heroes',
                'data': assignees
            }
            return Response(response, status=status.HTTP_200_OK)
            return Response(assignees)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)

# pm wise project list
class PmProjectList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        # try:
        #     projects = Projects.objects.filter(pm=pk)
        #     serializer = ProjectDetailsSerializer(projects, many=True)
        #     response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'PM Project List',
        #                 'data': serializer.data}
        # except Exception as e:
        #     response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        # return Response(response)
        try:
            projects_data = []
            traversed_projects = []
            assigned_projects = Projects.objects.filter(pm=pk)
            for project in assigned_projects:
                temp_project = project
                if temp_project.work_package_number not in traversed_projects:
                    traversed_projects.append(temp_project.work_package_number)
                    subtask_query_set = Projects.objects.filter(work_package_number=temp_project.work_package_number)
                    # print('subtasks',subtask_query_set)
                    subtasks = []
                    assignees = []
                    if len(subtask_query_set) > 0:
                        for task in subtask_query_set:
                            serialized_task = TaskSerializer(task).data
                            temp_assignees = ProjectAssigneeSerializer(ProjectAssignee.objects.filter(project=task.id),
                                                                       many=True).data
                            serialized_task['assignees'] = temp_assignees
                            subtasks.append(serialized_task)
                            for assignee in temp_assignees:
                                assignees.append(
                                    UserDetailSerializer(CustomUser.objects.get(pk=assignee['assignee']['id'])).data)

                    unique_assignees = unique(assignees)
                    serializer = ProjectDetailsSerializer(temp_project)
                    # print(assignees)
                    temp_data = {
                        'assignees': unique_assignees,
                        'project': serializer.data,
                        'subtasks': subtasks
                    }
                    projects_data.append(temp_data)
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Assigned Project List for a pm',
                        'data': projects_data}
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# assigned project list for employee
class AssignedProjectList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            projects_data = []
            traversed_projects = []
            assigned_projects = ProjectAssignee.objects.filter(assignee=pk).select_related('project')
            for project in assigned_projects:
                temp_project = Projects.objects.get(pk=project.project_id)
                if temp_project.work_package_number not in traversed_projects:
                    traversed_projects.append(temp_project.work_package_number)
                    subtask_query_set = Projects.objects.filter(work_package_number=temp_project.work_package_number)
                    # print('subtasks',subtask_query_set)
                    subtasks = []
                    assignees = []
                    if len(subtask_query_set) > 0:
                        for task in subtask_query_set:
                            serialized_task = TaskSerializer(task).data
                            temp_assignees = ProjectAssigneeSerializer(ProjectAssignee.objects.filter(project=task.id),
                                                                       many=True).data
                            serialized_task['assignees'] = temp_assignees
                            subtasks.append(serialized_task)
                            for assignee in temp_assignees:
                                assignees.append(
                                    UserDetailSerializer(CustomUser.objects.get(pk=assignee['assignee']['id'])).data)

                    unique_assignees = unique(assignees)
                    serializer = ProjectDetailsSerializer(temp_project)
                    # print(assignees)
                    temp_data = {
                        'assignees': unique_assignees,
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


class ChangePM(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self,request):
        try:
            Projects.objects.filter(work_package_number=request.data['wp']).update(pm=request.data['pm'])
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Project Manager changed'}
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


# assigned project list for employee
class ProjectWiseFileList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            serializerData = []
            user_info = CustomUser.objects.get(id=pk)
            if user_info.groups.filter(name='employee').exists():
                project_list = Projects.objects.values('work_package_number').distinct()
                for project_info in project_list:
                    project_details = Projects.objects.filter(work_package_number=project_info['work_package_number']).first()
                    projectAssigneeInfo = ProjectAssignee.objects.get(assignee=pk, project=project_details.id)
                    if projectAssigneeInfo:
                        project_ids = projectAssigneeInfo.project_id
                        projectInfo = Projects.objects.get(id=project_ids)
                        file_info = ProjectSharedFiles.objects.filter(work_package_number=projectInfo.work_package_number)
                        file_serializer = DocumentListSerializer(file_info, many=True)
                        serilizer = ProjectDetailsSerializer(projectInfo)
                        total_serializer = {"project": serilizer.data, "files": file_serializer.data}
                        serializerData.append(total_serializer)

            if user_info.groups.filter(name='pm').exists():
                project_list = Projects.objects.values('work_package_number').distinct()

                for project_info in project_list:
                    project_details = Projects.objects.filter(work_package_number=project_info['work_package_number']).first()
                    projectAssigneeInfo = ProjectAssignee.objects.get(assignee=pk, project=project_details.id)
                    if projectAssigneeInfo:
                        project_ids = projectAssigneeInfo.project_id
                        projectInfo = Projects.objects.get(id=project_ids)
                        file_info = ProjectSharedFiles.objects.filter(work_package_number=projectInfo.work_package_number)
                        file_serializer = DocumentListSerializer(file_info, many=True)
                        serilizer = ProjectDetailsSerializer(projectInfo)

                        assignee_serilizer = {"project": serilizer.data, "files": file_serializer.data}
                    pm_project_list = Projects.objects.filter(id=projectAssigneeInfo.project_id, pm=pk).first()
                    if projectAssigneeInfo.assignee != pm_project_list.pm:
                        projectInfo = Projects.objects.get(id=pm_project_list.id)
                        file_info = ProjectSharedFiles.objects.filter(
                            work_package_number=projectInfo.work_package_number)
                        pmfile_serializer = DocumentListSerializer(file_info, many=True)
                        pmserilizer = ProjectDetailsSerializer(projectInfo)
                        serializerData = {"project": pmserilizer.data, "files": pmfile_serializer.data}
                    serializerData.append(assignee_serilizer)
                        #
                        # for pm_project in pm_project_list:
                        #     project_details = Projects.objects.filter(work_package_number=pm_project['work_package_number']).first()
                        #     assinee_check_exist = ProjectAssignee.objects.get(assignee=project_details.pm, project=project_details.id)
                        #     if not assinee_check_exist:
                        #         projectInfo = Projects.objects.get(id=project_details.id)
                        #         print(projectInfo)
                        #         file_info = ProjectSharedFiles.objects.filter(
                        #             work_package_number=projectInfo.work_package_number)
                        #         pmfile_serializer = DocumentListSerializer(file_info, many=True)
                        #         pmserilizer = ProjectDetailsSerializer(projectInfo)
                        #         total_pm_serializer = {"project": pmserilizer.data, "files": pmfile_serializer.data}
                        #         serializerData.append(total_pm_serializer)


                    # pmproject = Projects.objects.filter(pm=pk)
                    # pmprojectserilizer = ProjectWiseFileListSerializer(pmproject, many=True)
                    # pmprojectserilizerData = pmprojectserilizer.data
                    # projectAssigneeInfo = ProjectAssignee.objects.filter(assignee=pk)
                    # serializerData = []
                    # for project_info in projectAssigneeInfo:
                    #     project_ids = project_info.project_id
                    #     assignee_ids = project_info.assignee_id
                    #     pmprojectcheck = Projects.objects.filter(pm=assignee_ids, id=project_ids)
                    #     if not pmprojectcheck:
                    #         projectInfo = Projects.objects.get(id=project_ids)
                    #         serilizer = ProjectWiseFileListSerializer(projectInfo)
                    #         serializerData.append(serilizer.data)
                # print(pmprojectserilizerData)
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Shared Document List For Each Project',
                        'data': serializerData}
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)

class ProjectWiseFileInsert(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        work_package_number = request.data.get('work_package_number')
        upload_by = request.data.get('upload_by')
        files = int(request.data.get('files')) + 1

        for i in range(1, files):
            indexval = str(i)
            attribute_name = str('file' + indexval)
            file = request.data.get(attribute_name)
            requested_data = {"work_package_number": work_package_number, "file": file, "upload_by": upload_by}
            serializer = ProjectFileSerializer(data=requested_data)
            if serializer.is_valid():
                serializer.save()
            else:
                serializer.errors()
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Document Insert Successful'
        }
        return Response(response)


class ChangeProjectStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self,request,pk):
        try:
            Projects.objects.filter(work_package_number=pk).update(status=request.data['status'])
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Project Status updated',
                        }
            return Response(response)

        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


class RemoveAssignee(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self,request,pk):
        try:
            print(request.data)
            # print(ProjectAssignee.objects.filter(assignee=request.data['assignee'], project=request.data['project']))
            ProjectAssignee.objects.filter(assignee=request.data['assignee'], project=request.data['project']).delete()
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Assignee removed',
                        }
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

class ProjectManagerList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        all_pm = UserDetailSerializer(CustomUser.objects.filter(groups__name='pm'), many=True).data
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Project Manager List',
            'data': all_pm
        }
        return Response(response)

class WPList(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        try:
            work_package_numbers = Projects.objects.values_list('work_package_number',flat=True)
            sub_tasks = Projects.objects.values_list('sub_task',flat=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'wp': unique(work_package_numbers),'sub_tasks':unique(sub_tasks)}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


class CheckWPandSubTask(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,sub_task,wp):
        try:
            wp_exists=False
            sub_task_exixts=False
            if Projects.objects.filter(work_package_number=wp).exists():
                wp_exists=True

            if Projects.objects.filter(sub_task=sub_task).exists():
                sub_task_exixts=True
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'wp_found': wp_exists, 'sub_task_found':sub_task_exixts}
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)