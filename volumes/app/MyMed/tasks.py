import os
from celery import shared_task as task


@task
def backup(self):
    os.system("python manage.py dbbackup")
