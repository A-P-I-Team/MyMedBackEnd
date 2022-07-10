from datetime import datetime, timedelta
from math import remainder
import threading
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from DocAndPatient.models import Reminder

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()




@shared_task
def SendEmail(EmailBody,Subject,From,To):
    email = EmailMessage(
        Subject,
        EmailBody,
        From,
        To,
            )
    email.content_subtype = "html"
    email.fail_silently = False
    EmailThread(email).run()




@shared_task
def Send_Reminder_Email():
    print("Send_Reminder_Email_____________________***********************______________________")
    myreminders=Reminder.objects.filter(date_time__gte=datetime.now()+timedelta(minutes=15),date_time__lte=datetime.now()+timedelta(minutes=30))
    for item in myreminders:
        pres_medicine=item.prescription_medicine
        medicine_name=pres_medicine.medicine.name
        user_name=pres_medicine.prescription.patient.first_name + " " + pres_medicine.prescription.patient.last_name
        doctor_name=pres_medicine.prescription.doctor.first_name + " " + pres_medicine.prescription.doctor.last_name
        if(user_name == None):
            user_name=pres_medicine.prescription.patient.username
        if(doctor_name == None):
            user_name=pres_medicine.prescription.doctor.username
        time=item.date_time
        user_email=pres_medicine.prescription.patient.username

        email_body = render_to_string("Email_Templates/email_reminder.html",{"medicine_name":medicine_name,"user_name":user_name,"doctor_name":doctor_name,'time':time})
        SendEmail.delay(email_body,'Reminder','MyMed',[user_email])



