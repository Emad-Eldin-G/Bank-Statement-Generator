from django.urls import path, include
from .views import *

urlpatterns = [
    path('pdf', main, name='GetPdf'),
]