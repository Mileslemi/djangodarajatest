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
    # on successful pay, what is sent to your callbackurl is and ResultCode=0
    # {"Body":
    #  {"stkCallback":
    #   {"MerchantRequestID":"98358-32664279-1",
    #    "CheckoutRequestID":"ws_CO_13102022154520280706803305",
    #    "ResultCode":0,
    #    "ResultDesc":"The service request is processed successfully.",
    #    "CallbackMetadata":
    #        {"Item":
    #          [
    #            {"Name":"Amount","Value":1.00},
    #            {"Name":"MpesaReceiptNumber","Value":"QJD4T7ZOT0"},
    #            {"Name":"Balance"},
    #            {"Name":"TransactionDate","Value":20221013154544},
    #            {"Name":"PhoneNumber","Value":254706803305}
    #          ]
    #        }
    #   }
    #  }
    # }

    # on time out, and ResultCode == 1037
    # {"Body":
    #   {"stkCallback":
    #     {"MerchantRequestID":"98357-32706531-1",
    #      "CheckoutRequestID":"ws_CO_13102022155941641714596833",
    #      "ResultCode":1037,
    #      "ResultDesc":"DS timeout user cannot be reached"
    #      }
    #    }
    # }

    # if cancelled by user ResultCode == 1032
    # {"Body":{"stkCallback":{"MerchantRequestID":"98371-32721597-1","CheckoutRequestID":"ws_CO_13102022160444963706803305","ResultCode":1032,"ResultDesc":"Request cancelled by user"}}}

    #  if user enters wrong pin ResultCode == 2001
    # {"Body":{"stkCallback":{"MerchantRequestID":"20561-30631158-1","CheckoutRequestID":"ws_CO_13102022160809538706803305","ResultCode":2001,"ResultDesc":"The initiator information is invalid."}}}
    # if user not m-pesa registered
    # {"Body":{"stkCallback":{"MerchantRequestID":"120570-20495815-1","CheckoutRequestID":"ws_CO_13102022164603749736005983","ResultCode":2001,"ResultDesc":"The initiator information is invalid."}}}
    return Response(response)