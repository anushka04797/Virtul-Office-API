import datetime
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organizations.serializers import DmaCalenderSerializer, HolidayCalenderSerializer, HourTypeSerializer
from .models import DmaCalender, HolidayCalender, HourType
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.serializers import UserDetailSerializer


class DmaCalenderDetails(APIView):
    permission_classes = (AllowAny,)
    serializer_class = DmaCalenderSerializer

    def get(self, request):
        try:
            calender = DmaCalender.objects.all()
            serializer = DmaCalenderSerializer(calender, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'DMA calender Details',
                        'data': serializer.data}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)

        return Response(response)


class HolidayCalenderDetails(APIView):
    permission_classes = (AllowAny,)
    serializer_class = HolidayCalenderSerializer

    def get(self, request):
        try:
            calender = HolidayCalender.objects.all()
            serializer = HolidayCalenderSerializer(calender, many=True)
            response = {'success': 'True', 'status code': status.HTTP_200_OK, 'message': 'DMA calender Details',
                        'data': serializer.data}
        except Exception as e:
            response = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), str(e)

        return Response(response)


class HoursSpentAndLeft(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = UserDetailSerializer(request.user).data
            user_company=user['slc_details']['slc']['department']['company']['id']
            result = []

            hour_types = HourTypeSerializer(HourType.objects.filter(company=user_company), many=True).data
            # for type in
            return Response(hour_types, status=status.HTTP_200_OK)
        except Exception as e:
            response = 'on line {}'.format(
                sys.exc_info()[-1].tb_lineno), str(e)
            return Response(response)
