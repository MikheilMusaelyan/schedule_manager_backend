from celery import shared_task
from time import sleep

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from rest_framework.response import Response

@shared_task
def sleepy():
    sleep(1)
    return None
