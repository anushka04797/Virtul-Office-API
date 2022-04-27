from datetime import date
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.utils import timezone, dateformat
from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sys
import os
import pendulum
import datetime

from projects.serializers import CreateProjectAssigneeSerializer, UpdateProjectRemainingHrsSerializer, \
    ProjectDetailsSerializer, ProjectAssigneeSerializer
from users.models import CustomUser
from users.serializers import UserDetailSerializer
from virtual_office_API.settings import EMAIL_HOST_USER
from wbs.serializers import CreateTimeCardSerializer, CreateWbsSerializer, WbsDetailsSerializer, WbsUpdateSerializer, \
    TimeCardDetailsSerializer, WbsStatusUpdateSerializer, WbsWiseTimeCardListSerializer, TimecardUpdateSerializer, \
    WbsFileSerializer
from wbs.models import TimeCard, Wbs
from projects.models import Projects, ProjectAssignee
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


# create wbs
class CreateWbs(APIView):
    serializer_class = CreateWbsSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request.data)
        assignee_list = request.data['assignee']
        for assignee in assignee_list:
            request.data['assignee'] = int(assignee)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_email = UserDetailSerializer(CustomUser.objects.get(id=assignee)).data['email']
            print(user_email)
            message = "A WBS titled '" + serializer.data[
                'title'] + "' has been assigned to you. Please check the Virtual Office for details."
            send_mail('WBS Created', message, EMAIL_HOST_USER, [user_email],
                      fail_silently=False, )
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'WBS created  successfully',
            'data': [serializer.data]
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


# wbs details
class WbsDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            wbs = Wbs.objects.get(id=pk)
            serializer = WbsDetailsSerializer(wbs)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'WBS Details',
                        'data': serializer.data}
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# update wbs
class UpdateWbs(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, pk, format=None):
        # print(request.data)
        try:
            wbs = Wbs.objects.get(id=pk)
            temp_data = request.data
            temp_data['date_updated'] = dateformat.format(timezone.now(), 'Y-m-d')
            # print(temp_data)
            serializer = WbsUpdateSerializer(wbs, data=temp_data)
            # print(serializer.errors)
            if serializer.is_valid():
                serializer.save()
                print(request.data)
                if serializer.data:
                    temp = {
                        "project": request.data['project'],
                        "wbs": serializer.data['id'],
                        "time_card_assignee": request.data['assignee'],
                        "actual_work_done": request.data['actual_work_done'],
                        "hours_today": request.data['hours_worked'],
                    }
                    serializer2 = CreateTimeCardSerializer(data=temp)
                    serializer2.is_valid()
                    print(serializer2.errors)
                    if serializer2.is_valid():
                        serializer2.save()
                        temp2 = {
                            "remaining_hours": request.data['remaining_hours']
                        }
                        project = Projects.objects.get(id=request.data['project'])
                        serializer3 = UpdateProjectRemainingHrsSerializer(project, data=temp2)
                        if serializer3.is_valid():
                            serializer3.save()
                            print(serializer.data)
                            user_email = \
                                UserDetailSerializer(CustomUser.objects.get(id=serializer.data['assignee'])).data[
                                    'email']
                            message = "A WBS titled '" + serializer.data[
                                'title'] + "' has been updated. Please check the Virtual Office for details."
                            send_mail('WBS Updated', message, EMAIL_HOST_USER, [user_email],
                                      fail_silently=False, )
                            response = {
                                'success': 'True',
                                'status code': status.HTTP_200_OK,
                                'message': 'wbs Updated Successful',
                                'data': serializer.data
                            }
                            return Response(response, status=status.HTTP_200_OK)
                        else:
                            response = {
                                'success': 'False',
                                'status code': status.HTTP_400_BAD_REQUEST,
                                'message': 'failed to update remaining hours'
                            }
                            return Response(response, status=status.HTTP_200_OK)
                    else:
                        response = {
                            'success': 'False',
                            'status code': status.HTTP_400_BAD_REQUEST,
                            'message': 'failed to insert in time card'
                        }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors)
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


# update wbs status
class UpdateWbsStatus(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, pk, format=None):
        # print(request.data)
        try:
            wbs = Wbs.objects.get(id=pk)
            temp_data = request.data
            temp_data['date_updated'] = dateformat.format(timezone.now(), 'Y-m-d')
            # print(temp_data)
            serializer = WbsStatusUpdateSerializer(wbs, data=temp_data)
            # print(serializer.errors)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'wbs Updated Successful',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors)
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


# WBS list for employee
class WbsListForEmployee(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            wbsList = Wbs.objects.filter(assignee=pk).order_by('-date_updated')
            Serializer = WbsDetailsSerializer(wbsList, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Assigned WBS List for an employee',
                        'data': Serializer.data}
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response({'success': 'False', 'status code': status.HTTP_400_BAD_REQUEST, 'message': 'Bad Request'})


# project wise WBS list
class WbsListForProject(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            wbsList = Wbs.objects.filter(work_package_number=pk).order_by('-date_updated')
            Serializer = WbsDetailsSerializer(wbsList, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Assigned WBS List for a project',
                        'data': Serializer.data}
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# Pm wise WBS list
class AllWbsListForPm(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            pm_project_list = Projects.objects.filter(pm=pk).order_by('date_updated')
            pm_project_list_serializer = ProjectDetailsSerializer(data=pm_project_list, many=True)
            pm_project_list_serializer.is_valid()
            temp_data = []
            temp_id = []
            for project in pm_project_list_serializer.data:
                # print(project['sub_task'])
                pm_wbs_list = Wbs.objects.filter(project=project['id']).order_by('-id')
                # print(pm_wbs_list)
                serializer2 = WbsDetailsSerializer(data=pm_wbs_list, many=True)
                serializer2.is_valid()
                for wbs in serializer2.data:
                    temp_data.append(wbs)
                    temp_id.append(wbs['id'])

            assignee_project_list = ProjectAssignee.objects.filter(assignee=pk).order_by('date_updated')
            assignee_project_list_serializer = ProjectAssigneeSerializer(data=assignee_project_list, many=True)
            assignee_project_list_serializer.is_valid()
            # print("temp_project_id_list", assignee_project_list_serializer.data)
            for project in assignee_project_list_serializer.data:
                if project['project'] is not None:
                    print("temp_project_id_list", project['project']['id'])
                    pm_wbs_list = Wbs.objects.filter(project=project['project']['id']).order_by('-id')
                    serializer2 = WbsDetailsSerializer(data=pm_wbs_list, many=True)
                    serializer2.is_valid()
                    for wbs in serializer2.data:
                        if wbs['id'] not in temp_id:
                            print('true')
                            temp_data.append(wbs)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'PM wise WBS List',
                        'data': temp_data}
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# Whole WBS list of assigned projects of an employee
class AllUserWbsListOfProject(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            wbs_project_list = []
            temp = []
            assigned_projects = ProjectAssignee.objects.filter(assignee=pk).order_by('-date_updated')
            serializer = CreateProjectAssigneeSerializer(assigned_projects, many=True)
            for AssignedProject in serializer.data:
                assigned_wbs_list = Wbs.objects.filter(project=AssignedProject['project']).order_by('-id')
                wbs_project_list.append(assigned_wbs_list)
            for wbs_list in wbs_project_list:
                serializer2 = WbsDetailsSerializer(wbs_list, many=True)
                for wbs in serializer2.data:
                    temp.append(wbs)
            # print(temp)
            response = {'success': 'True', 'status code': status.HTTP_200_OK,
                        'message': 'Assigned WBS List for a project',
                        'data': temp}
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# completed WBS count for a project
class CompletedWbsVsTotalCount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            completed_wbs_count = Wbs.objects.filter(
                work_package_number=pk, status=4).count()
            total_wbs_count = Wbs.objects.filter(
                work_package_number=pk).count()
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'Completed WBS count for a project',
                'data': {
                    "completed_wbs": completed_wbs_count,
                    "total_wbs": total_wbs_count
                }
            }
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# create time card
class CreateTimeCard(APIView):
    serializer_class = CreateTimeCardSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Time card created successfully',
            'data': []
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


# time card details
class TimeCardDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            time_card = TimeCard.objects.get(id=pk)
            serializer = TimeCardDetailsSerializer(time_card)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'time card details',
                        'data': serializer.data}
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


class AllTimeCards(APIView):
    permission_classes = (IsAuthenticated,)

    # def get(self,request,pk):
    # try:
    # time_cards = TimeCard.objects.filter()


# wbs wise time card list
class WbsWiseTimeCardList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            time_card = TimeCard.objects.filter(wbs=pk).order_by('-date_updated')
            serializer = WbsWiseTimeCardListSerializer(time_card, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'time card for a WBS',
                        'data': serializer.data}
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# user wise time card list
class UserWiseTimeCardList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            time_card = TimeCard.objects.filter(time_card_assignee=pk).order_by('-date_updated')
            serializer = WbsWiseTimeCardListSerializer(time_card, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'time card for a user',
                        'data': serializer.data}
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# user wise time card list
class UserWiseWeeklyTimeCardList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            pendulum.week_starts_at(pendulum.SUNDAY)
            pendulum.week_ends_at(pendulum.SATURDAY)
            today = pendulum.now()
            print(today.start_of('week'))
            start = today.start_of('week')
            print(start.to_datetime_string())
            end = today.end_of('week')
            print(end.to_datetime_string())
            time_card = TimeCard.objects.filter(time_card_assignee=pk, date_updated__gte=start,
                                                date_updated__lte=end).order_by('date_updated')
            serializer = WbsWiseTimeCardListSerializer(time_card, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'time card for a user',
                        'data': serializer.data, 'start_date': start, 'end_date': end}
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


class TimecardUpdate(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, pk, format=None):
        try:
            print(request.data)
            timecard = TimeCard.objects.get(id=pk)
            temp_data = request.data
            temp_data['date_updated'] = dateformat.format(timezone.now(), 'Y-m-d')
            print(temp_data)
            serializer = TimecardUpdateSerializer(timecard, data=temp_data)
            if serializer.is_valid():
                print(serializer.errors)
                serializer.save()
                response = {
                    'success': 'True',
                    'status code': status.HTTP_200_OK,
                    'message': 'timecard Updated Successful',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'success': 'False',
                    'status code': status.HTTP_400_BAD_REQUEST,
                    'message': 'failed to update timecard'
                }
                return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


class AddTimeCard(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateTimeCardSerializer

    def post(self, request):
        try:
            data = {
                'time_type': request.data['hours_type'],
                'actual_work_done': request.data['actual_work_done'],
                'submitted': 0,
                'hours_today': request.data['hours'],
                'project': request.data['project'],
                'wbs': request.data['wbs'],
                'time_card_assignee': request.data['assignee'],
                'date_created': datetime.datetime.now().date(),
                'date_updated': datetime.datetime.now().date()
            }
            print(data)
            new_time_card = self.serializer_class(data=data)
            new_time_card.is_valid(raise_exception=True)
            new_time_card.save()

            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'Timecard added Successfully',
                'data': new_time_card.data
            }
            return Response(response)
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)


class SubmitTimeCard(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        for item in request.data['time_cards']:
            TimeCard.objects.filter(pk=item).update(submitted=True)

        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Time Cards Submitted Successfully',
            'data': 'Time Cards Submitted'
        }
        return Response(response, status=status.HTTP_200_OK)


class UploadWbsDocs(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        upload_by = request.data.get('upload_by')
        files = int(request.data.get('files')) + 1

        for i in range(1, files):
            indexval = str(i)
            attribute_name = str('file' + indexval)
            file = request.data.get(attribute_name)
            requested_data = {"wbs_id": request.data.get('wbs_id'), "file": file, "upload_by": upload_by}
            serializer = WbsFileSerializer(data=requested_data)
            if serializer.is_valid():
                serializer.save()
            else:
                serializer.errors()

        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'WBS docs uploaded',
            'data': 'Time Cards Submitted'
        }
        return Response(response, status=status.HTTP_200_OK)

