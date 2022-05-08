from django.contrib import admin
from django.urls import path,include,re_path
from .views import *


app_name='DocAndPatient'

urlpatterns = [
    path('my_doctors/', User_Doctors_List.as_view(), name='User_Doctors_List'),
    path('doctors/', ListCreateDoctor.as_view(), name='ListCreateDoctor'),
    path('doctors/<int:pk>/', RetriveDoctor.as_view(), name='RetriveDoctor'),
]
