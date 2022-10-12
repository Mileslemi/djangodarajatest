import requests
from requests import auth
from requests.auth import HTTPBasicAuth
from django.conf import settings

def generate_access_token():
    results = requests.get(settings.ACCESS_TOKEN_URL, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY,settings.MPESA_CONSUMER_SECRET))
    response = results.json()
    print(response)
    access_token = response["access_token"]
    return access_token