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
from django.contrib.auth.hashers import make_password 
from django.db.models import Sum
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


schema_view = get_swagger_view(title='Pastebin API')
res={
     200:'Success request',
     201:'Success creation request',
     400: 'Bad request',
     403:'Invalid token (Forbidden)',
     404: 'Not found request',
     405: 'Unauthrized user ( doesn\'t have the permission to access this API )',
     409: 'Duplicate request',
     422: 'Invalid schema '
     }

@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username','password', 'email', 'Role'],
        properties={
            "username":openapi.Schema(type=openapi.TYPE_STRING,default="Abdo"),
            "password":openapi.Schema(type=openapi.TYPE_STRING,default="123456"),
            "email":openapi.Schema(type=openapi.TYPE_STRING,default="Abdo@gmail.com"),
            "Role":openapi.Schema(type=openapi.TYPE_STRING,default="Provider")
        },
    ),
    operation_description='Register new user' ,
    responses=res
)
@api_view(['POST'])
def signup(request):
    content_type = ContentType.objects.get_for_model(LoanRestProject.models.User)
    permissions=Permission.objects.filter(content_type=content_type)
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
            return Response({"Error":"Invalid user role"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            user = LoanRestProject.models.User.objects.get(username=request.data['username'])
            token = Token.objects.create(user=user)
            if user.role=='PROVIDER':
                for perm in permissions:
                    if perm.codename=='view_inboundloans' or perm.codename=='add_inboundloans':
                        user.user_permissions.add(perm)
                        user.save()
            elif user.role=='CUSTOMER':
                for perm in permissions:
                    if perm.codename=='view_outboundloans' or perm.codename=='add_outboundloans' or perm.codename=='add_payment':
                        user.user_permissions.add(perm)
                        user.save()    
            elif user.role=='PERSONNEL':
                for perm in permissions:
                    if perm.codename=='view_outboundloans' or perm.codename=='view_inboundloans' or perm.codename=='add_bankparameter':
                        user.user_permissions.add(perm)
                        user.save()
            return Response({'token': token.key, 'user':serializer.data['username']},status.HTTP_201_CREATED)
        else:
             return Response({"Error":"user name is already exist"}, status=status.HTTP_409_CONFLICT)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username','password'],
        properties={
            "username":openapi.Schema(type=openapi.TYPE_STRING,default="Abdo"),
            "password":openapi.Schema(type=openapi.TYPE_STRING,default="123456")
        },
    ),
    operation_description='Login user' ,
    responses=res
)
@api_view(['POST'])
def login(request):
    user = get_object_or_404(LoanRestProject.models.User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = FullUserserilizer(user)

    return Response({'token': token.key, 'user': serializer.data},status.HTTP_200_OK)


# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
    # print(request.auth )
    # user_id = Token.objects.get(key=request.auth.key).user_id
    # user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    # print(user.has_perm('LoanRestProject.view_inboundloans'))
    # print(user.user_permissions)
    # print(request.user)
    # return Response("passed!")

@swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "ProviderID":openapi.Schema(type=openapi.TYPE_STRING,default="1"),
        },
    ),
    
    operation_description='Get all inbound loans for current provider (provider profile) --- Get all inbound loans for provider id in body (Personnel profile) ' ,
    responses=res
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@permission_required('LoanRestProject.view_inboundloans')
def get_inbound_loan_list(request):
    # user_id = Token.objects.get(key=request.auth.key).user_id
    user_id=request.user.id
    # print(user_id)
    # print(request.user.id)
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)
    if serializer.data['role'] == 'PERSONNEL':
        if "ProviderID" not in request.data:
            return Response({"Error":"Invalid schema"},status.HTTP_422_UNPROCESSABLE_ENTITY)
        user_id=request.data['ProviderID']
    # inboundloans=InboundLoan.objects.all()
    inboundloans=InboundLoan.objects.filter(ProviderID=user_id)
    total=0
    count=0
    for inboundloan in inboundloans:
        total+=inboundloan.Amount
        count+=1

    serializer=InboundLoanSerializer(inboundloans , many=True)
    return Response({'Total number of loans':count,'Total loans amount':total,'inboundloans' : serializer.data},status.HTTP_200_OK)

@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['Amount'],
        properties={
            "Amount":openapi.Schema(type=openapi.TYPE_STRING,default="10000"),
        },
    ),
    operation_description='Create an Inbound Loan' ,
    responses=res
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@permission_required('LoanRestProject.add_inboundloans')
def post_inbound_loan(request):
    # user_id = Token.objects.get(key=request.auth.key).user_id
    user_id=request.user.id
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)
    request.data['ProviderID']=user_id
    serializer=InboundLoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response({'Error':'INVALID SCHEMA VALIDATION'},status.HTTP_422_UNPROCESSABLE_ENTITY)

@swagger_auto_schema(

    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['MinAmount','MaxAmount','NumberOfPayments','InterestRate'],
        properties={
            "MinAmount":openapi.Schema(type=openapi.TYPE_INTEGER,default="10000"),
            "MaxAmount":openapi.Schema(type=openapi.TYPE_INTEGER,default="10000"),
            "NumberOfPayments":openapi.Schema(type=openapi.TYPE_INTEGER,default="10000"),
            "InterestRate":openapi.Schema(type=openapi.TYPE_INTEGER,default="10000")
        },
    ),
    operation_description='Create an Inbound Loan' ,
    responses=res

)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@permission_required('LoanRestProject.add_bankparameter')
def post_bank_parameter(request):
    user_id=request.user.id
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)

    Bank.objects.all().delete()
    request.data['CustomerID']=user_id
    serializer=BankSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response({'Error':'INVALID SCHEMA VALIDATION'},status.HTTP_422_UNPROCESSABLE_ENTITY)


@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['Amount'],
        properties={
            "Amount":openapi.Schema(type=openapi.TYPE_STRING,default="10000"),

        },
    ),
    operation_description='Create an Outboand Loan' ,
    responses=res
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@permission_required('LoanRestProject.add_outboundloans')
def post_outbound_loan(request):
    # user_id = Token.objects.get(key=request.auth.key).user_id
    user_id=request.user.id
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)

    if "Amount" not in request.data.keys():
        return Response({'Error':'INVALID SCHEMA VALIDATION'},status.HTTP_422_UNPROCESSABLE_ENTITY)


    r_amount=request.data['Amount']
    bank=Bank.objects.get()
    bankserilizer=BankSerializer(bank)
    interest_amount=(r_amount*int(bankserilizer.data['InterestRate']))/100

    inboundloans_sum=InboundLoan.objects.aggregate(Sum('Amount'))
    # print(inboundloans_sum)
    unpaidoutboundloans_sum=OutboundLoan.objects.aggregate(Sum('UnpaidAmount'))
    # print(unpaidoutboundloans_sum)

    if inboundloans_sum['Amount__sum'] == None:
        inboundloans_sum['Amount__sum']=0
        
    if unpaidoutboundloans_sum['UnpaidAmount__sum'] == None:
        unpaidoutboundloans_sum['UnpaidAmount__sum']=0

    net_bank_balance=float(inboundloans_sum['Amount__sum'])-float(unpaidoutboundloans_sum['UnpaidAmount__sum'])
    if int(r_amount) < int(bankserilizer.data['MinAmount']) or r_amount > int(bankserilizer.data['MaxAmount']) or r_amount > net_bank_balance:
            return Response({'Error':'INVALID Amount according to bank parameters'},status.HTTP_400_BAD_REQUEST)
    
    
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
        return Response({'Error':'INVALID SCHEMA VALIDATION'},status.HTTP_422_UNPROCESSABLE_ENTITY)



@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "CustomerID":openapi.Schema(type=openapi.TYPE_STRING,default="1"),
        },
    ),
    operation_description='Get all inbound loans for current CUSTOMER (provider profile) --- Get all inbound loans for CustomerID id in body (Personnel profile) ' ,
    responses=res
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@permission_required('LoanRestProject.view_outboundloans')
def get_outbound_loan_list(request):
    user_id=request.user.id
    # print(user_id)
    # print(request.user.id)
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)
    if serializer.data['role'] == 'PERSONNEL':
        if "CustomerID" not in request.data:
            return Response({"Error":"Invalid schema"},status.HTTP_422_UNPROCESSABLE_ENTITY)
        user_id=request.data['CustomerID']

    # inboundloans=InboundLoan.objects.all()
    outboundloans=OutboundLoan.objects.filter(CustomerID=user_id)
    total=0
    count=0

    for outboundloan in outboundloans:
        total+=outboundloan.UnpaidAmount
        count+=1

    serializer=OutboundLoanSerializer(outboundloans , many=True)
    return Response({'Total number of loans':count,'Total unpaid loans amount':total,'outboundloans' : serializer.data},status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['LoanID'],
        properties={
            "LoanID":openapi.Schema(type=openapi.TYPE_STRING,default="10000"),

        },
    ),
    operation_description='Create an Outboand Loan PAYMENT' ,
    responses=res
    )
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@permission_required('LoanRestProject.add_payment')
def post_payment(request):
    user_id=request.user.id
    user = get_object_or_404(LoanRestProject.models.User, id=user_id)
    serializer=FullUserserilizer(user)
    if "LoanID" not in request.data.keys():
        return Response({'Error':'INVALID SCHEMA VALIDATION'},status.HTTP_422_UNPROCESSABLE_ENTITY)


    loanID=request.data['LoanID']
    # outboundloans=OutboundLoan.objects.filter(ID=loanID)
    outboundLoans=get_object_or_404(LoanRestProject.models.OutboundLoan,ID=loanID)
    serializer=OutboundLoanSerializer(outboundLoans)
    # serializer.data['PaidAmount']=1000
    if int(user_id) != int(serializer.data['CustomerID']):
        return Response({"Error":"This is not your loan"},status.HTTP_400_BAD_REQUEST)
    if int(serializer.data['NumberOfUnPaidPayments']) == 0  :
        return Response({"Error":"There is no payment required for this loan"},status.HTTP_400_BAD_REQUEST)
    
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
        return Response({'Error':'INVALID SCHEMA VALIDATION'},status.HTTP_422_UNPROCESSABLE_ENTITY)

