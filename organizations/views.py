import datetime
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organizations.serializers import DmaCalenderSerializer
from .models import DmaCalender
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
