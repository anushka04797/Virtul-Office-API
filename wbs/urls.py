from django.urls import path
from wbs.views import CreateWbs, WbsDetails, UpdateWbs, WbsListForEmployee, CreateTimeCard, TimeCardDetails, \
    CompletedWbsVsTotalCount, WbsListForProject, AllUserWbsListOfProject, UpdateWbsStatus, WbsWiseTimeCardList, \
    UserWiseTimeCardList, AllWbsListForPm, UserWiseWeeklyTimeCardList

urlpatterns = [
    path('create/', CreateWbs.as_view()),
    path('details/<str:pk>/', WbsDetails.as_view()),
    path('update/<str:pk>/', UpdateWbs.as_view()),
    path('update/status/<str:pk>/', UpdateWbsStatus.as_view()),
    path('user/all/<str:pk>/', WbsListForEmployee.as_view()),
    path('pm/all/<str:pk>/', AllWbsListForPm.as_view()),
    path('all/<str:pk>/', AllUserWbsListOfProject.as_view()),
    path('project/all/<str:pk>/', WbsListForProject.as_view()),
    path('completed/<str:pk>/', CompletedWbsVsTotalCount.as_view()),
    path('time-card/create/', CreateTimeCard.as_view()),
    path('time-card/details/<str:pk>/', TimeCardDetails.as_view()),
    path('time-card/list/<str:pk>/', WbsWiseTimeCardList.as_view()),
    path('user/time-card/list/<str:pk>/', UserWiseTimeCardList.as_view()),
    path('user-wise/weekly-time-card/<str:pk>/', UserWiseWeeklyTimeCardList.as_view()),
]
