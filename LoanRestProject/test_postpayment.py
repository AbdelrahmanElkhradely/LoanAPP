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

class postpaymentTestClass(TestCase):
    correct_token=''
    @classmethod
    def setUpClass(cls):
        super(postpaymentTestClass, cls).setUpClass()

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
            "NumberOfPayments":2,
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

    def test_postpayment_success_201(self):

        print("successfully post payment")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Customeruserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postpayment="/LoanApp/postpayment"
        data={"LoanID":"1"}
        response=client.post(url_postpayment,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    def test_postpayment_fail_422(self):

        print("failing posting a payment due to schema error")
        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Customeruserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postpayment="/LoanApp/postpayment"
        data={"wrongschema":"1"}
        response=client.post(url_postpayment,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_422_UNPROCESSABLE_ENTITY)
   
    def test_postpayment_fail_302(self):

        print("fail to make a payment using provider profile (permission denied)")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Provideruserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postpayment="/LoanApp/postpayment"
        data={"LoanID":"1"}
        response=client.post(url_postpayment,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_302_FOUND)



    def test_postpayment_fail_302(self):

        print("failing Posting a payment due to loan not found")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Customeruserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postpayment="/LoanApp/postpayment"
        data={"LoanID":"1000"}
        response=client.post(url_postpayment,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_postpayment_fail_400(self):

        print("fail to make a paymeent as this loan has no remaining payments")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "Customeruserrr","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)

        for i in range(2):
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION=self.correct_token)
            url_postpayment="/LoanApp/postpayment"
            data={"LoanID":"1"}
            response=client.post(url_postpayment,data,format='json')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_postpayment="/LoanApp/postpayment"
        data={"LoanID":"1"}
        response=client.post(url_postpayment,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


