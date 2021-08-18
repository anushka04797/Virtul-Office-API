from datetime import date
from django.contrib.auth.models import Group
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sys
import os
from wbs.serializers import CreateWbsSerializer, WbsDetailsSerializer, WbsUpdateSerializer
from wbs.models import Wbs
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
    permission_classes = (IsAuthenticated,)

    def post(self, request):
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
            wbs = Wbs.objects.filter(id=pk)
            serializer = WbsDetailsSerializer(wbs, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'WBS Details',
                        'data': serializer.data}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
        return Response(response)


# update wbs
class UpdateWbs(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):
        # print(request.data)
        try:
            wbs = Wbs.objects.get(id=pk)
            serializer = WbsUpdateSerializer(wbs, data=request.data)
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
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)