from django.urls import path
from .views import CreateProject, ProjectDetails, UpdateProject, PmProjectList, AssignedProjectList, ProjectAssigneeList

urlpatterns = [
    path('create/', CreateProject.as_view()),
    path('details/<str:pk>/', ProjectDetails.as_view()),
    path('update/<str:pk>/', UpdateProject.as_view()),
    path('all/<str:pk>/', PmProjectList.as_view()),
    path('assigned/all/<str:pk>/', AssignedProjectList.as_view()),
    path('assignee/list/<str:pk>/', ProjectAssigneeList.as_view()),
    # path('add/assignee/', AddProjectAssignee.as_view()),
    # path('remove/assignee/', RemoveProjectAssignee.as_view()),
]
