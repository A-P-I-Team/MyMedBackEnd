from django.contrib import admin
from django.urls import path,include,re_path
from .views import *


app_name='DocAndPatient'

urlpatterns = [
    path('doctors/', User_Doctors_List.as_view(), name='User_Doctors_List'),

]