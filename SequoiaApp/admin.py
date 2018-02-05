from django.contrib import admin
from .models import Customer, Remitter, RTGS
# Register your models here.

admin.site.register(Customer)
admin.site.register(Remitter)
admin.site.register(RTGS)
