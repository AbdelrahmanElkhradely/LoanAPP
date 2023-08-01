from django.http import JsonResponse
import LoanRestProject
from .models import *

from .Serializers import *

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password ,check_password
from django.db.models import Sum

@api_view(['POST'])
def signup(request):
    request.data['password']=make_password(request.data['password'])
    serializer = TempUserSerializer(data=request.data)
    if serializer.is_valid():
        if request.data['Role'] == 'Provider':
            serializer = ProviderSerializer(data=request.data)
        elif request.data['Role'] == 'Customer':
            serializer = CustomerSerializer(data=request.data)
        elif request.data['Role'] == 'Personnel':
            serializer = PersonnelSerializer(data=request.data)
        else:
            return Response({"Error":"Invalid user type"}, status=status.HTTP_200_OK)
        
        if serializer.is_valid():
            serializer.save()
            user = LoanRestProject.models.User.objects.get(username=request.data['username'])
            token = Token.objects.create(user=user)
            print(serializer.data)
            return Response({'token': token.key, 'user':serializer.data['username']})
        else:
             return Response({"Error":"Invalid data"}, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(LoanRestProject.models.User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = FullUserserilizer(user)

    return Response({'token': token.key, 'user': serializer.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    print(request.auth )
    user_id = Token.objects.get(key=request.auth.key).user_id
    print(request.user)
    return Response("passed!")

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_inbound_loan_list(request):
    # user_id = Token.objects.get(key=request.auth.key).user_id
    user_id=request.user.id
    # print(user_id)
    # print(request.user.id)
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)
    if serializer.data['role'] == 'PERSONNEL':
        if "ProviderID" not in request.data:
            return Response({"Error":"Invalid schema"})
        user_id=request.data['ProviderID']

    elif serializer.data['role'] == 'CUSTOMER':
        return Response({"Error":"You are not authorized"})
    # inboundloans=InboundLoan.objects.all()
    inboundloans=InboundLoan.objects.filter(ProviderID=user_id)
    total=0
    count=0

    for inboundloan in inboundloans:
        total+=inboundloan.Amount
        count+=1

    serializer=InboundLoanSerializer(inboundloans , many=True)
    return JsonResponse({'Total number of loans':count,'Total loans amount':total,'inboundloans' : serializer.data})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_inbound_loan(request):
    # user_id = Token.objects.get(key=request.auth.key).user_id
    user_id=request.user.id
    request.data['ProviderID']=user_id
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)

    if serializer.data['role'] != 'PROVIDER':
        return Response({"Error":"You are not authorized"})
    
    serializer=InboundLoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response({'Error':'INVALID SCHEMA VALIDATION'})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_bank_parameter(request):
    user_id=request.user.id
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)
    if serializer.data['role'] != 'PERSONNEL':
        return Response({"Error":"You are not authorized"})
    else:
        Bank.objects.all().delete()
        request.data['CustomerID']=user_id
        serializer=BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Error':'INVALID SCHEMA VALIDATION'})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_outbound_loan(request):
    # user_id = Token.objects.get(key=request.auth.key).user_id
    user_id=request.user.id
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)
    if serializer.data['role'] != 'CUSTOMER':
        return Response({"Error":"You are not authorized"})
    
    r_amount=request.data['Amount']
    bank=Bank.objects.get()
    bankserilizer=BankSerializer(bank)
    interest_amount=(r_amount*int(bankserilizer.data['InterestRate']))/100

    inboundloans_sum=InboundLoan.objects.aggregate(Sum('Amount'))
    print(inboundloans_sum)
    unpaidoutboundloans_sum=OutboundLoan.objects.aggregate(Sum('UnpaidAmount'))
    print(unpaidoutboundloans_sum)

    if inboundloans_sum['Amount__sum'] == None:
        inboundloans_sum['Amount__sum']=0
        
    if unpaidoutboundloans_sum['UnpaidAmount__sum'] == None:
        unpaidoutboundloans_sum['UnpaidAmount__sum']=0

    net_bank_balance=float(inboundloans_sum['Amount__sum'])-float(unpaidoutboundloans_sum['UnpaidAmount__sum'])
    print(net_bank_balance)
    if int(r_amount) < int(bankserilizer.data['MinAmount']) or r_amount > int(bankserilizer.data['MaxAmount']) or r_amount > net_bank_balance:
            return Response({'Error':'INVALID Amount according to bank parameters'})
    
    
    request.data['CustomerID']=user_id
    request.data['TotalNumberOfPaymets']=int(bankserilizer.data['NumberOfPayments']) 
    request.data['PaymentAmount']=(r_amount+interest_amount)/int(bankserilizer.data['NumberOfPayments']) 
    request.data['NumberOfPaidPayments']=0
    request.data['NumberOfUnPaidPayments']=int(bankserilizer.data['NumberOfPayments']) 
    request.data['PaidAmount']=0
    request.data['InterestAmount']=interest_amount
    request.data['UnpaidAmount']=r_amount+interest_amount
    serializer=OutboundLoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response({'Error':'INVALID SCHEMA VALIDATION'})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_outbound_loan_list(request):
    user_id=request.user.id
    # print(user_id)
    # print(request.user.id)
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)
    if serializer.data['role'] == 'PERSONNEL':
        if "CustomerID" not in request.data:
            return Response({"Error":"Invalid schema"})
        user_id=request.data['CustomerID']

    elif serializer.data['role'] == 'PROVIDER':
        return Response({"Error":"You are not authorized"})
    # inboundloans=InboundLoan.objects.all()
    outboundloans=OutboundLoan.objects.filter(CustomerID=user_id)
    total=0
    count=0

    for outboundloan in outboundloans:
        total+=outboundloan.UnpaidAmount
        count+=1

    serializer=OutboundLoanSerializer(outboundloans , many=True)
    return JsonResponse({'Total number of loans':count,'Total unpaid loans amount':total,'outboundloans' : serializer.data})




@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_payment(request):
    user_id=request.user.id
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)
    if serializer.data['role'] != 'CUSTOMER':
        return Response({"Error":"You are not authorized"})
    else:
        loanID=request.data['LoanID']
        # outboundloans=OutboundLoan.objects.filter(ID=loanID)
        outboundLoans=get_object_or_404(LoanRestProject.models.OutboundLoan,ID=loanID)
        serializer=OutboundLoanSerializer(outboundLoans)
        # serializer.data['PaidAmount']=1000
        print(serializer.data)
        if int(user_id) != int(serializer.data['CustomerID']):
            return Response({"Error":"This is not your loan"})

        if int(serializer.data['NumberOfUnPaidPayments']) == 0  :
            return Response({"Error":"There is no payment required for this loan"})
        
        request.data['Amount']=serializer.data['PaymentAmount']
        request.data['CustomerID']=user_id
        paymentserializer=PaymentSerializer(data=request.data)
        
        if paymentserializer.is_valid():
            paymentserializer.save()
            outboundLoans.PaidAmount+=serializer.data['PaymentAmount']
            outboundLoans.UnpaidAmount-=serializer.data['PaymentAmount']
            outboundLoans.NumberOfUnPaidPayments-=1
            outboundLoans.NumberOfPaidPayments+=1

            outboundLoans.save()
            return Response(paymentserializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Error':'INVALID SCHEMA VALIDATION'})

