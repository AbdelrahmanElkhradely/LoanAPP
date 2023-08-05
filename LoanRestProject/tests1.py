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

class ProviderTestClass(TestCase):
    
    def test_provider_success(self):
        #success script
        token='testtoken'
        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }
        data_req={"username": "provider","password": "Pass1234!", "email": "adam@mail.com","Role":"Provider"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


        url_login="/LoanApp/login"
        data={ "username": "provider","password": "Pass1234!"}
        # client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response=client.post(url_login, data, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response_json=json.loads(response.content)
        token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=token)


        url_postinboundloan="/LoanApp/postinboundloans"
        data={ "Amount": 10000 }
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


        url_postinboundloan="/LoanApp/getinboundloans"
        data={}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_registration_fail(self):
        #DUPLICATE CREATION FOR USER
        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }
        data_req={"username": "qpp","password": "Pass1234!", "email": "adam@mail.com","Role":"Provider"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


        data_req={"username": "qpp","password": "Pass1234!", "email": "adam@mail.com","Role":"Provider"}
        response=client.post(url_register, data_req, format='json')
        self.assertEqual(response.status_code,status.HTTP_409_CONFLICT)


        url_login="/LoanApp/login"
        data={ "username": "qpp","password": "Wrong password"}
        response=client.post(url_login, data, format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)













# class LoginTest(TestCase):
#     login_url="/LoanApp/getinboundloans"
#     def setUp(self):
#         self.user=User.objects.create_user(username="bido",password="123456")

#         self.token=Token.objects.create(user=self.user)

#         self.api_authentaction()
    
#     def api_authentaction(self):
#         self.client.credentials(HTTP_AUTHORIZATION="TOKEN "+self.token.key)
    
#     def test_login(self):
#         response=self.client.post(self.login_url)
#         print("hiiiiiiiii")
#         self.assertEqual(response.status_code,status.HTTP_200_OK)


