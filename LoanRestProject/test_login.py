from base64 import decode
from django.test import TestCase

import json
import LoanRestProject

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
import requests

from LoanRestProject.Serializers import UserSerializer

from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

# from .models import *

class LoginTestClass(TestCase):
        
    def test_login_success_200(self):
        client = APIClient()
        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }

        data_req={"username": "user","password": "Pass1234!", "email": "adam@mail.com","Role":"Provider"}
        response=client.post(url_register, data_req, format='json')

        print("user success full login")
        client = APIClient()
        url_login="/LoanApp/login"
        data={"username": "user","password": "Pass1234!"}
        # client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response=client.post(url_login, data, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_login_success_404(self):
        print("user failure login due to incorrect user name or password")
        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "WRONG USER NAME","password": "WRONG PASSWORD"}
        response=client.post(url_login, data, format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)