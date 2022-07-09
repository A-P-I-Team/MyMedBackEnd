from celery import shared_task
from DocAndPatient.models import Reminder
from datetime import datetime, timedelta



@shared_task
def Set_Reminder_Flase_After_Time():
    myreminders=Reminder.objects.filter(date_time__gte=datetime.now()-timedelta(hours=1),date_time__lte=datetime.now()-timedelta(minutes=30))
    for item in myreminders:
        if(item.status == None):
            item.status=False
            item.save()
    