import threading
from celery import shared_task
from django.core.mail import EmailMessage


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