from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage

import os
from django.conf import settings
import json
from datetime import datetime
from docxtpl import DocxTemplate
from docx2pdf import convert
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

    #Rendering the template with the data fetched from database
    template.render({'email': email, 'total': total, 'fromDate': date1, 'toDate': date2, 'invoice_list': transactionsList})
    template.save(os.path.join(settings.BASE_DIR, f'api/invoices/{email}-{date1}-{date2}.docx'))
    return


def sendEmail(data):
    #In production, the email address and password will be fetched from environment variables
    #address = os.environ.get('EMAIL_ADDRESS')
    #password = os.environ.get('EMAIL_PASSWORD')
    address = "omda.gasser@gmail.com"
    #password = "" #for security reasons, the password will not be included in the code

    #creating the email message
    msg = EmailMessage()
    msg['Subject'] = f'Zywa Invoice {data["date1"]} - {data["date2"]}'
    msg['From'] = address
    #msg['To'] = f"{data['email']}" #Will be sent to real email in production
    msg['To'] = "omda.g@outlook.com" #For testing purposes
    msg.set_content('Dear valued customer,\n\nPlease find your requested transaction details.\nThank you for using our services,\nTeam Zywa')

    #converting the invoice from docx to pdf
    convert(os.path.join(settings.BASE_DIR, f'api/invoices/{data["email"]}-{data["date1"]}-{data["date2"]}.docx'), os.path.join(settings.BASE_DIR, f'api/invoices/{data["email"]}-{data["date1"]}-{data["date2"]}.pdf'))

    #reading the raw binary data from the invoice to attach it to the email
    with open(os.path.join(settings.BASE_DIR, f'api/invoices/{data["email"]}-{data["date1"]}-{data["date2"]}.pdf'), 'rb') as f:
        file_data = f.read()
        file_name = f'{data["email"]}-{data["date1"]}-{data["date2"]}.pdf'
        msg.add_attachment(file_data, maintype='application/pdf', subtype='octet-stream', filename=file_name)

    #sending the email using the gmail smtp server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(address, password)
        smtp.send_message(msg)


@api_view(['POST'])
def main(request):
    data = json.loads(request.body)

    #creation of invoice happens in invoiceGenerator service
    invoiceGenerator(data)

    #sending email using the sendEmail service
    sendEmail(data)

    return JsonResponse({'message': 'Post request sent successfully'})