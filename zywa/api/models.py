from django.db import models
from django.contrib.postgres import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.core import serializers
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.serializers import ModelSerializer, Serializer

# Create your models here.

class bankUser(models.Model):
    email =     models.EmailField(null=True)

    def __str__(self) -> str:
        return self.email


class transaction(models.Model):
    user    =    models.ForeignKey('bankUser', on_delete=models.CASCADE)
    sale    =    models.FloatField(null=True)
    details =    models.TextField(null=True)
    amount  =    models.FloatField(null=True)
    date    =    models.DateField(null=True)

    def __str__(self) -> str:
        return f"{self.details} - {self.date}"
