from django.shortcuts import redirect
from requests import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

def redirect_view(request):
    response = redirect('/admin/')
    return response



