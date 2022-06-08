from django.contrib import admin
from django.urls import path, include, re_path
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'DocAndPatient'

router = DefaultRouter()
router.register('medicines', MedicineViewSet, basename='Medicines')
router.register('prescriptions', PrescriptionViewSet, basename='Prescriptions')
router.register('prescription-medicines', PrescriptionMedicinesViewSet, 'PrescriptionMedicines')

urlpatterns = [
    path('my_doctors/', User_Doctors_List.as_view(), name='User_Doctors_List'),
    path('doctors/', ListCreateDoctor.as_view(), name='ListCreateDoctor'),
    path('doctors/<int:pk>/', RetriveDoctor.as_view(), name='RetriveDoctor'),
    path('active-prescription-medicines/', ActivePrescriptionMedicinesAPIView.as_view(), name='ActivePrescriptionMedicines'),
    path('reminders/<int:pk>/', ReminderAPIView.as_view(), name='Reminder')
]

urlpatterns += router.urls
