from django.shortcuts import render
from django.apps import apps
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMessage
import json
import jinja2
import pdfkit
import os

@api_view(['POST'])
def getPdf(request):
    data = json.loads(request.body)

    email = EmailMessage(
        f"Transaction details {data['date-in']} - {data['date-out']}",
        'Please check below',
        'omda.g@outlook.com',
        [f"{data['email']}"],
    )

    context = {
        "email": data['email'],
        "data-in": data['date-in'],
        "data-out": data['date-out'],
    }

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template("pdf.html")
    output = template.render(context)

    options = {
    'page-size': 'A4',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
    'encoding': 'UTF-8'
}

    pdfkit.from_string(output, "output.pdf", options=options, configuration=pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

    email.attach(output.pdf, 'application/pdf')
    email.send()

    os.remove("output.pdf")

    return Response(status=status.HTTP_200_OK)