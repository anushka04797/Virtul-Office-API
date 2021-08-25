from django.urls import path
from wbs.views import CreateWbs, WbsDetails, UpdateWbs, CreateTimeCard, TimeCardDetails


urlpatterns = [
    path('create/', CreateWbs.as_view()),
    path('details/<str:pk>/', WbsDetails.as_view()),
    path('update/<str:pk>/', UpdateWbs.as_view()),
    path('time-card/create/', CreateTimeCard.as_view()),
    path('time-card/details/<str:pk>/', TimeCardDetails.as_view()),
]
