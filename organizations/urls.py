from django.urls import path
from .views import DmaCalenderDetails, HolidayCalenderDetails

urlpatterns = [
    path('calender/all/', DmaCalenderDetails.as_view()),
    path('holiday/all/', HolidayCalenderDetails.as_view()),
]
