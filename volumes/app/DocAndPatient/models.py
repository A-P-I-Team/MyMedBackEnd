from django.db import models
from User.models import User
# Create your models here.




class Doctor(User):
    work_field=models.CharField(max_length=30, null=True, blank=True)
    Medical_system_number=models.CharField(max_length=30, null=True, blank=True)
    experience=models.IntegerField(null=True, blank=True)
    about=models.TextField(null=True, blank=True)
    hours_of_work=models.CharField(max_length=200, null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    phone_number=models.CharField(max_length=200, null=True, blank=True)
    office_number=models.CharField(max_length=200, null=True, blank=True)
    latitude=models.DecimalField(max_digits=9, decimal_places=6 , null=True, blank=True)
    longitude=models.DecimalField(max_digits=9, decimal_places=6 , null=True, blank=True)
    