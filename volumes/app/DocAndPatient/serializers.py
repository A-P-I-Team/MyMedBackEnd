from rest_framework import serializers
from DocAndPatient.models import *
from User.models import User


class DoctorSerializer(serializers.ModelSerializer):
    pass


class SimpleDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'degree', 'field']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'birthdate']


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['name', 'type']


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['doctor', 'patient', 'description', 'date_time']


class PrescriptionMedicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionMedicines
        fields = ['medicine', 'prescription', 'unit_price', 'count']


class GetPrescriptionMedicinesSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)

    class Meta:
        model = PrescriptionMedicines
        fields = ['medicine', 'unit_price', 'count']


class GetPrescriptionSerializer(serializers.ModelSerializer):
    doctor = SimpleDoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    medicines = GetPrescriptionMedicinesSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ['doctor', 'patient', 'description', 'date_time', 'medicines']

