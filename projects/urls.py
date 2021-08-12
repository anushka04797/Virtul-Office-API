from django.urls import path
from .views import CreateProject, ProjectDetails, UpdateProject

urlpatterns = [
    path('create/', CreateProject.as_view()),
    path('details/<str:pk>/', ProjectDetails.as_view()),
    path('update/<str:pk>/', UpdateProject.as_view()),
    # path('add/assignee/', AddProjectAssignee.as_view()),
    # path('remove/assignee/', RemoveProjectAssignee.as_view()),
]
