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

class postinboundloanTestClass(TestCase):
    correct_token=''
    @classmethod
    def setUpClass(cls):
        super(postinboundloanTestClass, cls).setUpClass()

        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }
        data_req={"username": "provideruser","password": "Pass1234!", "email": "adam@mail.com","Role":"Provider"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')

        data_req={"username": "notprovideruser","password": "Pass1234!", "email": "adam@mail.com","Role":"Customer"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')

    def test_postinbound_success_201(self):

        print("successfully adding inbound loan")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "provideruser","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/postinboundloans"
        data={"Amount": 100000}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_postinbound_fail_422(self):
        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "provideruser","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)

        print("failing to add inboundloan due schema error")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)

        url_postinboundloan="/LoanApp/postinboundloans"
        data={ "Wrongschema": 100000 }
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_postinbound_fail_403(self):
        client = APIClient()
        
        print("failing to add inboundloan due invalid token")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='token 123455aaaaa')

        url_postinboundloan="/LoanApp/postinboundloans"
        data={ "Amount": 100000 }
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_postinbound_fail_405(self):

        print("failing adding inbound loan due to permission issue")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "notprovideruser","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/postinboundloans"
        data={"Amount": 100000}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_302_FOUND)

        # url_postinboundloan="/LoanApp/getinboundloans"
        # data={}
        # response=client.post(url_postinboundloan,data,format='json')
        # self.assertEqual(response.status_code,status.HTTP_200_OK)