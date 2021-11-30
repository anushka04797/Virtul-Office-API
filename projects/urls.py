from django.urls import path
from .views import CreateProject, ProjectDetails, UpdateProject, ChangePM, PmProjectList,PmProjectAllAssigneeList, AssignedProjectList, \
    ProjectAssigneeList, DeleteSubTask, ChangeTDOTitle, TdoList, NewProjectDetails, ChangeProjectStatus, RemoveAssignee, ProjectWiseFileList, ProjectWiseFileInsert, ProjectManagerList,WPList,CheckWPandSubTask

urlpatterns = [
    path('tdo/list/', TdoList.as_view()),
    path('create/', CreateProject.as_view()),
    path('details/<str:pk>/', NewProjectDetails.as_view()),
    path('update/<str:pk>/', UpdateProject.as_view()),
    path('all/<str:pk>/', PmProjectList.as_view()),
    path('assignees/all/<str:pk>/', PmProjectAllAssigneeList.as_view()),
    path('assigned/all/<str:pk>/', AssignedProjectList.as_view()),
    path('shared/document/list/<str:pk>/', ProjectWiseFileList.as_view()),
    path('shared/document/create/', ProjectWiseFileInsert.as_view()),
    path('assignee/list/<str:pk>/', ProjectAssigneeList.as_view()),
    path('subtask/delete/<str:work_package_index>/', DeleteSubTask.as_view()),
    path('change-tdo-title/<str:pk>/', ChangeTDOTitle.as_view()),
    path('change-status/<str:pk>/', ChangeProjectStatus.as_view()),
    path('remove-assignee/<str:pk>/', RemoveAssignee.as_view()),
    path('change-project-manager/', ChangePM.as_view()),
    # path('add/assignee/', AddProjectAssignee.as_view()),
    # path('remove/assignee/', RemoveProjectAssignee.as_view()),
    path('managers/', ProjectManagerList.as_view()),
    path('work-package-numbers/', WPList.as_view()),
    path('check-subtask-work-package-number-is-valid/<str:sub_task>/<str:wp>/', CheckWPandSubTask.as_view()),
]
