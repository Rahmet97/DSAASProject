import datetime
from time import sleep

from django.conf import settings
from django.db.models import Q
from .models import TGChannel
from celery import shared_task


@shared_task
def auto_post():
    sleep(10)
    try:
        print("123")
    except Exception as e:
        raise e
