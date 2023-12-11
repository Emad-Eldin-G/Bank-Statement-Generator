from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMessage

import os
from django.conf import settings
import json
from datetime import datetime
from docxtpl import DocxTemplate
from .models import transaction

def invoiceGenerator(data):
    email = data['email']
    date1 = data['date1']
    date2 = data['date2']

    #Initializing template to be used
    template = DocxTemplate(os.path.join(settings.BASE_DIR, "api/invoiceTemplate.docx"))

    #Getting transactions from database and turining them into a list
    transactions = transaction.objects.filter(user__email=email, date__range=[date1, date2])
    transactionsList = [list(i) for i in transactions.values_list('date', 'details', 'sale', 'amount')]

    total = 0
    for t in transactionsList:
        t[0] = t[0].strftime('%d/%m/%Y')
        total += t[3]
    #print(transactionsList)

    #Rendering the template with the data fetched from database
    template.render({'email': email, 'total': total, 'fromDate': date1, 'toDate': date2, 'invoice_list': transactionsList})
    template.save(os.path.join(settings.BASE_DIR, f'api/invoices/{email}-{date1}-{date2}.docx'))
    return


@api_view(['POST'])
def getPdf(request):
    data = json.loads(request.body)
    #creation of invoice happens in invoiceGenerator func
    invoiceGenerator(data)

    email = EmailMessage('Zywa Invoice', 
        'Hello valued customer, \n Please find your requested transaction details. \n Thank you for using our services, \n Team Zywa',
        'omda.g@outlook.com',
        ["omda.gasser@gmail.com"], 
        )

    #email.attach_file(os.path.join(settings.BASE_DIR, f'api/invoices/{data["email"]}-{data["date1"]}-{data["date2"]}.pdf'), 'application/pdf')

    try:
        #email.send()
        return Response("Good")
    except:
        return Response("Bad")