from datetime import date
from django.contrib.auth.models import Group
from django.utils import timezone, dateformat
from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sys
import os

from projects.serializers import CreateProjectAssigneeSerializer, UpdateProjectRemainingHrsSerializer
from wbs.serializers import CreateTimeCardSerializer, CreateWbsSerializer, WbsDetailsSerializer, WbsUpdateSerializer, \
    TimeCardDetailsSerializer, WbsStatusUpdateSerializer, WbsWiseTimeCardListSerializer
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
        print(request.data['assignee'])
        assignee_list = request.data['assignee']
        for assignee in assignee_list:
            request.data['assignee'] = assignee
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'WBS created  successfully',
            'data': []
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
            wbsList = Wbs.objects.filter(assignee=pk)
            Serializer = WbsDetailsSerializer(wbsList, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'Assigned WBS List for an employee',
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
            wbsList = Wbs.objects.filter(work_package_number=pk)
            Serializer = WbsDetailsSerializer(wbsList, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'Assigned WBS List for a project',
                            'data': Serializer.data}
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
            assigned_projects = ProjectAssignee.objects.filter(assignee=pk)
            serializer = CreateProjectAssigneeSerializer(assigned_projects, many=True)
            for AssignedProject in serializer.data:
                assigned_wbs_list = Wbs.objects.filter(project=AssignedProject['project'])
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


# wbs wise time card list
class WbsWiseTimeCardList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            time_card = TimeCard.objects.filter(wbs=pk)
            serializer = WbsWiseTimeCardListSerializer(time_card, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'time card for a WBS',
                        'data': serializer.data}
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)
