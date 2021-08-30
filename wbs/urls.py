from django.urls import path
from wbs.views import CreateWbs, WbsDetails, UpdateWbs, WbsListForEmployee, CreateTimeCard, TimeCardDetails, CompletedWbsVsTotalCount, WbsListForProject


urlpatterns = [
    path('create/', CreateWbs.as_view()),
    path('details/<str:pk>/', WbsDetails.as_view()),
    path('update/<str:pk>/', UpdateWbs.as_view()),
    path('user/all/<str:pk>/', WbsListForEmployee.as_view()),
    path('project/all/<str:pk>/', WbsListForProject.as_view()),
    path('completed/<str:pk>/', CompletedWbsVsTotalCount.as_view()),
    path('time-card/create/', CreateTimeCard.as_view()),
    path('time-card/details/<str:pk>/', TimeCardDetails.as_view()),
]
