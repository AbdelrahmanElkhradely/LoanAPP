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

class getinboundloanTestClass(TestCase):
    correct_token=''
    @classmethod
    def setUpClass(cls):
        super(getinboundloanTestClass, cls).setUpClass()

        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }
        data_req={"username": "provideruser","password": "Pass1234!", "email": "adam@mail.com","Role":"Provider"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')
        

        headerInfo = {'content-type': 'application/json' }
        data_req={"username": "PERSONNEL","password": "Pass1234!", "email": "adam@mail.com","Role":"Personnel"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')

        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }
        data_req={"username": "CUSTOMER","password": "Pass1234!", "email": "adam@mail.com","Role":"Customer"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')
        


        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "provideruser","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        correct_token='token '+response_json['token']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=correct_token)
        url_postinboundloan="/LoanApp/postinboundloans"
        data={"Amount": 100000}
        response=client.post(url_postinboundloan,data,format='json')

    def test_getinbound_success_200(self):

        print("successfully getting inbound loan")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "provideruser","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/getinboundloans"
        data={}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_getinbound_success_200(self):

        print("successfully getting inbound loan using personnel profile")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "PERSONNEL","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/getinboundloans"
        data={"ProviderID":1}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_getinbound_fail_422(self):

        print("failing getting inbound loan using personnel profile due to schema error")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "PERSONNEL","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/getinboundloans"
        data={"wrongschema":1}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_422_UNPROCESSABLE_ENTITY)
   
    def test_getinbound_success_302(self):

        print("failing getting inbound loans due to using customer profile")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "CUSTOMER","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/getinboundloans"
        data={"ProviderID":1}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_302_FOUND)