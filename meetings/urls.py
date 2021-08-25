from django.urls import path
from .views import CreateMeetings, MeetingsDetails, UpdateMeetings

urlpatterns = [
    path('create/', CreateMeetings.as_view()),
    path('details/<str:pk>/', MeetingsDetails.as_view()),
    path('update/<str:pk>/', UpdateMeetings.as_view()),
]
