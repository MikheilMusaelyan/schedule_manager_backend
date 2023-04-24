from celery import shared_task
from time import sleep

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from rest_framework.response import Response

@shared_task
def sleepy(request):
    sleep(request)
    return None

import smtplib
import ssl
from email.message import EmailMessage
from django.conf import settings

def send_email(subject, body):
    # Define email sender and receiver
    email_sender = settings.EMAIL_HOST_USER
    email_password = settings.EMAIL_HOST_PASSWORD
    email_receiver = settings.EMAILED_TO

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())        
