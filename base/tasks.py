from celery import shared_task
from time import sleep

import smtplib
import ssl
from email.message import EmailMessage
from django.conf import settings

@shared_task
def send_the_email():
    sleep(10)

    email_sender = settings.EMAIL_HOST_USER
    email_password = settings.EMAIL_HOST_PASSWORD

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = 'fullstackmasters0@gmail.com'
    em['Subject'] = 'subject'
    em.set_content('body')
    
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, 'fullstackmasters0@gmail.com', em.as_string())     