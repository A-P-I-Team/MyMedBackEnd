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

#_______________________________________________________________________________________


class ListDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'profile_pic', 'field']


class FullDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'ssn',
            'citizens_ssn',
            'gender',
            'birthdate',
            'profile_pic',
            'user_city',
            'relationship_status',
            'isVaccinated',
            'msn',
            'degree',
            'field',
            'experience',
            'about',
            'hours_of_work',
            'address',
            'phone',
            'officeno',
            'latitude',
            'longitude',

        )
        extra_kwargs = {
            'gender': {'required': False},
            'birthdate': {'required': False},
            'profile_pic': {'required': False},
            'msn': {'required': False},
            'degree': {'required': False},
            'field': {'required': False},
            'experience': {'required': False},
            'about': {'required': False},
            'hours_of_work': {'required': False},
            'address': {'required': False},
            'phone': {'required': False},
            'officeno': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
        }