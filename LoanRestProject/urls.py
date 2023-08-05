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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import include

schema_view = get_schema_view(
   openapi.Info(
      title="LoanAPP API",
      default_version='v1',
      description="BLNK task",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="a.elkhradely@gmail.com"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,

   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('downloadswaggerr/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('admin', admin.site.urls),
    re_path('getinboundloans',views.get_inbound_loan_list),
    re_path('postinboundloans',views.post_inbound_loan),
    re_path('postoutboundloans',views.post_outbound_loan),
    re_path('getoutboundloans',views.get_outbound_loan_list),
    re_path('postpayment',views.post_payment),
    re_path('setbankparameter',views.post_bank_parameter),
    re_path('register', views.signup),
    re_path('login', views.login),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    # re_path('test_token', views.test_token),
    # re_path('api_admin/', site.urls),
    # re_path('swagger', views.schema_view)
    
]

urlpatterns = [path(r'LoanApp/', include(urlpatterns))]

