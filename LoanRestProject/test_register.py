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
class RegisterTestClass(TestCase):

    def test_registration_Success_201(self):

        #CREATION FOR USER
        print("user succesfull creation test")
        client = APIClient()
        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }

        data_req={"username": "qpp","password": "Pass1234!", "email": "adam@mail.com","Role":"Provider"}
        response=client.post(url_register, data_req, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    def test_registration_fail_409(self):
        print("user failure creation test due to duplicate users")

        #DUPLICATE CREATION FOR USER
        client = APIClient()
        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }

        data_req={"username": "qpp","password": "Pass1234!", "email": "adam@mail.com","Role":"Provider"}
        response=client.post(url_register, data_req, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        data_req={"username": "qpp","password": "Pass1234!", "email": "adam@mail.com","Role":"Customer"}
        response=client.post(url_register, data_req, format='json')
        self.assertEqual(response.status_code,status.HTTP_409_CONFLICT)
        
        # url_login="/LoanApp/login"
        # data={ "username": "qpp","password": "Wrong password"}
        # response=client.post(url_login, data, format='json')
        # self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_registration_fail_400(self):
        print("user failure creation test due to invalid user role")

        #CREATION FOR USER with wrong role type
        client = APIClient()
        url_register="/LoanApp/register"
        headerInfo = {'content-type': 'application/json' }

        data_req={"username": "qpp","password": "Pass1234!", "email": "adam@mail.com","Role":"wrong type"}
        response=client.post(url_register, data_req, format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)