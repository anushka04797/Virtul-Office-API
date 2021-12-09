from django.urls import path
from .views import DmaCalenderDetails

urlpatterns = [
    path('calender/all/', DmaCalenderDetails.as_view()),
]
