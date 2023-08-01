"""
URL configuration for LoanRestProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from LoanRestProject import views
from django.urls import re_path
from django_api_admin.sites import site


urlpatterns = [
    path('admin', admin.site.urls),
    re_path('getinboundloans',views.get_inbound_loan_list),
    re_path('postinboundloans',views.post_inbound_loan),
    re_path('postoutboundloans',views.post_outbound_loan),
    re_path('getoutboundloans',views.get_outbound_loan_list),
    re_path('postpayment',views.post_payment),
    re_path('setbankparameter',views.post_bank_parameter),
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('test_token', views.test_token),
    re_path('api_admin/', site.urls)
    
]
