from django.urls import path
from .views import DmaCalenderDetails, HolidayCalenderDetails, HoursSpentAndLeft

urlpatterns = [
    path('calender/all/', DmaCalenderDetails.as_view()),
    path('holiday/all/', HolidayCalenderDetails.as_view()),
    path('user/hours/used-left/', HoursSpentAndLeft.as_view()),
]
