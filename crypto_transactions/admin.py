from django.contrib import admin
from .models import DebitTransaction, Address

# Register your models here.

admin.site.register(DebitTransaction)
admin.site.register(Address)

