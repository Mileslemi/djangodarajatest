import imp
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from requests import auth
from requests.auth import HTTPBasicAuth
from .utils import generate_access_token, generate_password,get_current_time, stk_push
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
     {
     'Desc':'View access token & password',
     'url':'localhost/generateAcessToken/'},
     {
     'Desc':'callback url, where resultd from daraja will be sent',
     'url':'your own https live domain'
     },
     {
     'Desc':'Stk Push',
     'url':'localhost/stk_push/'
     }
     ]
    return Response(routes)

@api_view(['GET'])
def viewTokenPassword(request):
    access_token = generate_access_token()
    theTimestamp = get_current_time()
    thePassword = generate_password(theTimestamp)
    return Response({"access_token":access_token, "Password":thePassword})

@api_view(['POST'])
def make_payment(request):
    data = request.data
    amount = data['amount']
    # valid m-pesa reg number
    phone_number = data['mobile']
    response = stk_push(amount=amount,number=phone_number)
    return Response(response)