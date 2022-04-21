import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.



# class Question(models.Model):
#     string_question=models.CharField(max_length=200)
#     string_answer=models.CharField(max_length=200,null=True, blank=True)
#     bool_answer=models.BooleanField(null=True, blank=True)

    
#     def __str__(self):
#         return self.user.all().first().username + ' - ' + self.string_question

class City(models.Model):
    city_name=models.CharField(max_length=200)
    def __str__(self):
        return self.city_name


class User(AbstractUser):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    password = models.CharField(
        blank=False,
        max_length=30,
        validators=[RegexValidator(regex="^(?=.*[A-Z])",message='Password must contain at least one uppercase letter.'),
            RegexValidator(regex="^(?=.*[0-9])",message='Password must contain at least one number.'),
            RegexValidator(regex="^(?=.{8,})",message='Password must be eight characters or longer.')]
        )
    username = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True,default=None)
    birthdate = models.DateField(null=True, blank=True,default=None)
    profile_pic = models.ImageField(upload_to='images/profile_pics/', null=True, blank=True,default=None)
    ssn = models.CharField(max_length=20,blank=True,unique=True,null=True)
    citizens_ssn = models.CharField(max_length=20,blank=True,unique=True,null=True)
    # questions = models.ManyToManyField(Question,related_name="user",blank=True)
    relationship_status = models.CharField(max_length=20,blank=True,null=True)
    isVaccinated = models.CharField(max_length=20,blank=True,null=True)


    user_city = models.ForeignKey(City,related_name="city",blank=True,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.username









