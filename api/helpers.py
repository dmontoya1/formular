import binascii
import os

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

from django.contrib.auth.middleware import get_user

def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()

def get_api_user(request): 
    if request:
        if request.auth:
            return request.auth.user
        return get_user(request)
    pass


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening