from celery import shared_task
from time import sleep

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from rest_framework.response import Response

@shared_task
def send_email():
    sleep(10)
    email = EmailMessage(
        'Celery task worked!',
        'Congratulations. Celery task & email sending worked. You are the best programmer in the world.',
        settings.EMAIL_HOST_USER,
        ['fullstackmasters0@gmail.com'],
    )
    email.fail_silently=False
    email.send()
    return None