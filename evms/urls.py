from django.urls import path
from .views import CreateEvms, WbsDetails, UpdateEvms

urlpatterns = [
    path('create/', CreateEvms.as_view()),
    path('details/<str:pk>/', WbsDetails.as_view()),
    path('update/<str:pk>/', UpdateEvms.as_view()),
]
