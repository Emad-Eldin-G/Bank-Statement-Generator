from django.contrib import admin
from .models import bankUser, transaction

# Register your models here.

admin.site.register(bankUser)
admin.site.register(transaction)