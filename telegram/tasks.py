import datetime
from time import sleep

from django.conf import settings
from django.db.models import Q
from .models import TGChannel, Post
from celery import shared_task


@shared_task
def auto_post():
    sleep(10)
    try:
        posts = Post.objects.filter(Q(date__lt=datetime.datetime.now()-datetime.timedelta(seconds=10)))

    except Exception as e:
        raise e
