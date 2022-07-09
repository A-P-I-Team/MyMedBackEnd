import os
from celery import shared_task
from django.core.management import call_command


@shared_task
def backup():
    try:
        call_command('dbbackup')
    except:
        pass







