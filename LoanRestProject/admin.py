from django.contrib import admin
from .models import *
from django_api_admin.sites import site

admin.site.register(InboundLoan)
admin.site.register(OutboundLoan)
admin.site.register(Bank)
admin.site.register(User)
admin.site.register(Payment)




