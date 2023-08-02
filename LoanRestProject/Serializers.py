
from rest_framework import serializers
import LoanRestProject
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = [ 'username', 'password', 'email','Role']

class TempUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = TempUser
        fields = [ 'username', 'password', 'email','Role']

class ProviderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Provider
        fields = [ 'username', 'password', 'email','Role']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Customer
        fields = [ 'username', 'password', 'email','Role']

class PersonnelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Personnel
        fields = [ 'username', 'password', 'email','Role']

class FullUserserilizer(serializers.ModelSerializer):
    class Meta(object):
        model=LoanRestProject.models.User
        fields = '__all__'

class InboundLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InboundLoan
        fields=['ID','Amount',
                'ProviderID',
                'CreateDate']

class OutboundLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutboundLoan
        fields=[
            'ID',
            'CustomerID',
            'Amount',
            'TotalNumberOfPaymets',
            'PaymentAmount',
            'NumberOfPaidPayments',
            'NumberOfUnPaidPayments',
            'PaidAmount','InterestAmount',
            'UnpaidAmount','CreateDate'
        ]
    
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields=[

            'ID',
            'MinAmount',
            'MaxAmount',
            'NumberOfPayments',
            'InterestRate',
            'CustomerID',
            'CreateDate'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields=[

            'ID',
            'Amount',
            'CustomerID',
            'LoanID',
            'CreateDate'
        ]
class ProviderIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = InboundLoan
        fields=[
            'ProviderID'
        ]


