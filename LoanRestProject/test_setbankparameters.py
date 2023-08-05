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

class postbankparamtersTestClass(TestCase):
    correct_token=''
    @classmethod
    def setUpClass(cls):
        super(postbankparamtersTestClass, cls).setUpClass()

        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }
        data_req={"username": "personneluser","password": "Pass1234!", "email": "adam@mail.com","Role":"Personnel"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')

        data_req={"username": "nonpersonnaluser","password": "Pass1234!", "email": "adam@mail.com","Role":"Customer"}
        client = APIClient()
        response=client.post(url_register, data_req, format='json')

    def test_postinbound_success_201(self):

        print("successfully adding bank parameters")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "personneluser","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_setbankparam="/LoanApp/setbankparameter"
        data={
            "MinAmount":100,
            "MaxAmount":1000,
            "NumberOfPayments":10,
            "InterestRate":5
            }
        response=client.post(url_setbankparam,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_postinbound_fail_422(self):
        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "personneluser","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)

        print("failing to add bank param due schema error")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)

        url_setbankparam="/LoanApp/setbankparameter"
        data={ "MinAmt":100,
            "NumberOfPa":10,
            "InterestRate":5 }
        response=client.post(url_setbankparam,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_postinbound_fail_403(self):
        client = APIClient()
        
        print("failing to add bank param due invalid token")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='token 123455aaaaa')

        url_setbankparam="/LoanApp/setbankparameter"
        data={
            "MinAmount":100,
            "MaxAmount":1000,
            "NumberOfPayments":10,
            "InterestRate":5
        }

        response=client.post(url_setbankparam,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_postinbound_fail_405(self):

        print("successfully setting bank param due to permission issue")

        client = APIClient()
        url_login="/LoanApp/login"
        data={ "username": "nonpersonnaluser","password": "Pass1234!"}
        response=client.post(url_login, data, format='json')
        response_json=json.loads(response.content)
        self.correct_token='token '+response_json['token']
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.correct_token)
        url_setbankparam="/LoanApp/setbankparameter"
        data={
            "MinAmount":100,
            "MaxAmount":1000,
            "NumberOfPayments":10,
            "InterestRate":5
        }
        response=client.post(url_setbankparam,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_302_FOUND)
