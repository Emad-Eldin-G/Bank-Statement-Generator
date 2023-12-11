from django.urls import path, include
from .views import *

urlpatterns = [
    path('pdf', getPdf, name='GetPdf'),
]