from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
User_Model = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
       username = input("username: ")
       password = input("password: ")
       ssn = input("ssn: ")
       User_Model.objects.create(username=username,password=password,ssn=ssn)

       