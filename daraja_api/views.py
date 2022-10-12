from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from requests import auth
from requests.auth import HTTPBasicAuth
from .access_mpesa_token import generate_access_token
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = ['View access tokens', 'callback url']
    return Response(routes)

@api_view(['GET'])
def viewAccessToken(request):
    access_token = generate_access_token()
    return Response({"access_token":access_token})