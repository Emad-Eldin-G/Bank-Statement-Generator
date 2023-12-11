from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMessage

import json
from docxtpl import DocxTemplate
from .models import transaction

def invoiceGenerator(data):
    email = data['email']
    date1 = data['date1']
    date2 = data['date2']

    template = DocxTemplate('zywa/api/templates/invoiceTemplate.docx')

    transactions = transaction.objects.filter(user__email=email, date__range=[date1, date2]).defer('user')
    transactionsList = list(transactions.values())

    template.render({'email': email, 'fromDate': date1, 'toDate': date2, 'invoice_list': transactionsList})
    template.pdf(f'zywa/api/invoices/{email}-{date1}-{date2}.pdf')
    return


@api_view(['POST'])
def getPdf(request):
    data = json.loads(request.body)
    invoiceGenerator(data)

    email = EmailMessage('Zywa Invoice', 
        'Hello valued customer, \n Please find your requested transaction details. \n Thank you for using our services, \n Team Zywa',
        'omda.g@outlook.com',
        ["omda.gasser@gmail.com"], 
        )

    email.attach_file(f'zywa/api/invoices/{data["email"]}-{data["date1"]}-{data["date2"]}.pdf', 'application/pdf')

    try:
        email.send()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)