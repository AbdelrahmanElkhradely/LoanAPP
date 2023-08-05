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

class getoutboundloanTestClass(TestCase):
    correct_token=''
    @classmethod
    def setUpClass(cls):
        super(getoutboundloanTestClass, cls).setUpClass()

        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }
        data_req={"username": "Customeruserrr","password": "Pass1234!", "email": "adam@mail.com","Role":"Customer"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')

        data_req={"username": "Provideruserrr","password": "Pass1234!", "email": "adam@mail.com","Role":"Provider"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')

        data_req={"username": "Personneluserrr","password": "Pass1234!", "email": "adam@mail.com","Role":"Personnel"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')


        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Provideruserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=correct_token)
        url_postinboundloan="/LoanApp/postinboundloans"
        data={"Amount": 100000}
        response=client.post(url_postinboundloan,data,format='json')


        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Personneluserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=correct_token)
        url_setbankparam="/LoanApp/setbankparameter"
        data={
            "MinAmount":100,
            "MaxAmount":5000,
            "NumberOfPayments":10,
            "InterestRate":5
        }
        response=client.post(url_setbankparam,data,format='json')

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Customeruserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=correct_token)
        url_postoutboundloan="/LoanApp/postoutboundloans"
        data={"Amount": 2000}
        response=client.post(url_postoutboundloan,data,format='json')

    def test_getoutbound_success_200(self):

        print("successfully getting outbound loan")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Customeruserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/getoutboundloans"
        data={}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_getoutboundloan_success_200(self):

        print("successfully getting outbound loan using personnel profile")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Personneluserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/getoutboundloans"
        data={"CustomerID":"1"}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_getoutbound_fail_422(self):

        print("failing getting outbound loan using personnel profile due to schema error")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Personneluserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/getoutboundloans"
        data={"wrongschema":"1"}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_422_UNPROCESSABLE_ENTITY)
   
    def test_getoutbound_fail_302(self):

        print("failing getting outbound loans due to using provider profile (permission denied)")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Provideruserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postinboundloan="/LoanApp/getoutboundloans"
        data={"CustomerID":"1"}
        response=client.post(url_postinboundloan,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_302_FOUND)

