from __future__ import absolute_import

import os
import django

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DSAAS.settings')
django.setup()

app = Celery('DSAAS')

app.conf.enable_utc = False
app.conf.update(timezone='Asia/Tashkent')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'auto_posting_telegram': {
        'task': 'telegram.tasks.auto_post',
        'schedule': 10
    },
    # 'auto_posting_instagram': {
    #     'task': 'instagram.tasks.auto_post',
    #     'schedule': 10
    # },
    # 'auto_posting_facebook': {
    #     'task': 'facebook.tasks.auto_post',
    #     'schedule': 10
    # }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
