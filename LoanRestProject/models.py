from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    class Role(models.TextChoices):
          ADMIN="ADMIN",'Admin'
          PROVIDER="PROVIDER",'Provider'
          CUSTOMER="CUSTOMER",'Customer'
          PERSONNEL="PERSONNEL",'Personnel'
    class Meta():
                permissions = (
            ('view_inboundloans', 'view inbounds'),
            ('add_inboundloans', 'add inboundloans'),
            ('view_outboundloans', 'view outboundloans'),
            ('add_outboundloans', 'add outboundloans'),
            ('add_payment', 'add payment'),
            ('add_bankparameter', 'add bankparameter'),
            
        )
    base_role=Role.ADMIN
    role=models.CharField(max_length=50,choices=Role.choices)

    def save(self,*args,**kwargs):
        if not self.pk:
            self.role=self.base_role
            return super().save(*args,**kwargs)


class ProviderManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PROVIDER)


class Provider(User):

    base_role = User.Role.PROVIDER

    Provider = ProviderManager()

    class Meta:
        proxy = True
        # permissions = (
        #     ('trail', 'Friendly permission description'),
        # )
    def welcome(self):
        return "Only for Providers"


class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)


class Customer(User):

    base_role = User.Role.CUSTOMER

    customer = CustomerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Customers"


class PersonnelManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PERSONNEL)


class Personnel(User):

    base_role = User.Role.PERSONNEL

    personnel = PersonnelManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for PersonnelS"

        
class InboundLoan(models.Model):
    ID=models.AutoField(primary_key=True)
    Amount=models.IntegerField()
    ProviderID=models.ForeignKey(User,on_delete=models.CASCADE)
    CreateDate=models.DateTimeField(auto_now_add=True)


class OutboundLoan(models.Model):
    ID=models.AutoField(primary_key=True)
    CustomerID=models.ForeignKey(User,on_delete=models.CASCADE)
    Amount=models.IntegerField()
    TotalNumberOfPaymets=models.IntegerField()
    PaymentAmount=models.FloatField()
    NumberOfPaidPayments=models.IntegerField()
    NumberOfUnPaidPayments=models.IntegerField()
    InterestAmount=models.FloatField()
    PaidAmount=models.FloatField()
    UnpaidAmount=models.FloatField()
    CreateDate=models.DateTimeField(auto_now_add=True)


class Bank(models.Model):
    ID=models.AutoField(primary_key=True)
    MinAmount=models.IntegerField()
    MaxAmount=models.IntegerField()
    NumberOfPayments=models.IntegerField()
    InterestRate=models.IntegerField()
    CustomerID=models.ForeignKey(User,on_delete=models.CASCADE)
    CreateDate=models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    ID=models.AutoField(primary_key=True)
    Amount=models.IntegerField()
    CustomerID=models.ForeignKey(User,on_delete=models.CASCADE)
    LoanID=models.ForeignKey(OutboundLoan, on_delete = models.CASCADE)
    CreateDate=models.DateTimeField(auto_now_add=True)


class TempUser(models.Model):
    ROLE_CHOICES = (
    ("Provider", "Provider"),
    ("Customer", "Customer"),
    ("Personnel", "Personnel")

    )
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=1000)
    email=models.CharField(max_length=100)
    Role=models.CharField(max_length=30,choices=ROLE_CHOICES)







