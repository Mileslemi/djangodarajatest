import json
from urllib import response
import requests
from requests import auth
from requests.auth import HTTPBasicAuth
from django.conf import settings
from datetime import datetime

import base64

def generate_access_token():
    results = requests.get(settings.ACCESS_TOKEN_URL, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY,settings.MPESA_CONSUMER_SECRET))
    response = results.json()
    # if successful - response is json of expiry_in, access_token
    print(response)
    access_token = response["access_token"]
    return access_token

def get_current_time():
    current_time = datetime.now()
    formated_time = current_time.strftime("%Y%m%d%H%M%S")
    # ----
    # Timestamp of the transaction, 
    # normaly in the formart of YEAR+MONTH+DATE+HOUR+MINUTE+SECOND (YYYYMMDDHHMMSS)
    # Each part should be atleast two digits apart from the year which takes four digits.
    return formated_time

def generate_password(date):
    # This is the password used for encrypting the request sent:
    #  A base64 encoded string. 
    # (The base64 string is a combination of Shortcode+Passkey+Timestamp)
    
    thePassword = settings.MPESA_EXPRESS_SHORTCODE + settings.MPESA_PASSKEY + date
    encodedPass = base64.b64encode(thePassword.encode())
    decodedPass = encodedPass.decode("utf-8")
    print(decodedPass)
    return decodedPass

def stk_push(amount, number):
    access_token = generate_access_token()
    timeStamp = get_current_time()
    password = generate_password(timeStamp)

    headers = {"Authorization":"Bearer %s" % access_token}
    # parameter required are in https://developer.safaricom.co.ke/APIs/MpesaExpressSimulate
    json_parameters = {
        'BusinessShortCode':settings.MPESA_EXPRESS_SHORTCODE,
        'Password':password,
        'Timestamp':timeStamp,
        'TransactionType':settings.TRANSACTION_TYPE,
        'Amount':amount,
        'PartyA':number,
        'PartyB':settings.MPESA_EXPRESS_SHORTCODE,
        'PhoneNumber':number,
        'CallBackURL':settings.CALLBACK_URL,
        'AccountReference':settings.ACCOUNT_REFERENCE,
        'TransactionDesc':settings.TRANSACTION_DESCRIPTION,
    }

    response = requests.post(settings.STK_PUSH_URL, json=json_parameters,headers=headers)

    responseString = response.text
    print(responseString)
    jsonResponse = json.loads(responseString)
    print(jsonResponse)
    # if stk push successful, you'll get a response with 
    # MerchantRequestID, CheckoutRequestID, ResponseDescription
    # ResponseCode(with 0 meaning successful), CustomerMessage
    # https://developer.safaricom.co.ke/APIs/MpesaExpressSimulate

    data = {
        "MerchantRequestID":jsonResponse['MerchantRequestID'],
        "CheckoutRequestID":jsonResponse['CheckoutRequestID'],
        "ResponseDescription":jsonResponse['ResponseDescription'],
        "ResponseCode":jsonResponse['ResponseCode'],
    }

    return data

