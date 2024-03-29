from datetime import datetime, timedelta, timezone
from rest_framework import serializers
from DocAndPatient.models import *
from User.models import User


class SimpleDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'profile_pic', 'degree', 'field']


class SimplePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'gender', 'birthdate']


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'type']


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'doctor', 'patient', 'description', 'date_time']


class PrescriptionMedicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionMedicines
        fields = ['id', 'medicine', 'prescription', 'dosage', 'fraction', 'days', 'description', 'start', 'period', 'notify']


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'date_time', 'status']
        read_only_fields = ['id', 'date_time']
        # fields = ['id', 'prescription_medicine', 'date_time', 'status']


class ListPrescriptionMedicinesSerializer(serializers.ModelSerializer):
    medicine = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PrescriptionMedicines
        fields = ['id', 'prescription', 'medicine', 'dosage', 'fraction', 'days' , 'start']


class ListPrescriptionMedicinesRemindersSerializer(serializers.ModelSerializer):
    medicine = serializers.StringRelatedField(read_only=True)
    reminders = ReminderSerializer(read_only=True, many=True)
    datetime = serializers.DateTimeField(read_only=True, source='prescription.date_time')

    class Meta:
        model = PrescriptionMedicines
        fields = ['id', 'prescription', 'datetime', 'medicine', 'dosage', 'fraction',
                  'days', 'start', 'period', 'reminders', 'takenno', 'notify', 'description']


class RetrievePrescriptionMedicinesSerializer(serializers.ModelSerializer):
    medicine = serializers.StringRelatedField(read_only=True)
    doctor = SimpleDoctorSerializer(source='prescription.doctor')

    elapsed = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def get_elapsed(self, pm: PrescriptionMedicines):
        # TODO: Check Formula Correctness: ElapsedTime
        return min((datetime.now(timezone.utc) - pm.start).days, pm.days) if pm.start else 0

    def get_remaining(self, pm: PrescriptionMedicines):
        # TODO: Check Formula Correctness: RemainingTime
        return max((pm.start + timedelta(days=pm.days) - datetime.now(timezone.utc)).days, 0) if pm.start else 0

    def get_progress(self, pm: PrescriptionMedicines):
        # TODO: Check Formula Correctness: ProgressTime
        # return round((datetime.now(timezone.utc) - pm.prescription.date_time).days / pm.days, 4) * 100
        return round(Reminder.objects.filter(
                prescription_medicine=pm.id,
                status=True
            ).count() / (24 * pm.days // pm.period), 2) * 100 if pm.start else 0

    def get_count(self, pm: PrescriptionMedicines):
        return 24 * pm.days // pm.period

    class Meta:
        model = PrescriptionMedicines
        fields = ['medicine', 'dosage', 'fraction', 'days', 'elapsed', 'remaining', 'progress',
                  'description', 'doctor', 'start', 'period', 'count', 'takenno', 'nottakenno', 'notify']


class PatientUpdatePrescriptionMedicinesSerializer(serializers.ModelSerializer):
    medicine = serializers.StringRelatedField(read_only=True)
    doctor = SimpleDoctorSerializer(source='prescription.doctor', read_only=True)
    reminders = ReminderSerializer(read_only=True, many=True)

    class Meta:
        model = PrescriptionMedicines
        fields = ['medicine', 'doctor', 'start', 'notify', 'reminders']


class DoctorUpdatePrescriptionMedicinesSerializer(serializers.ModelSerializer):
    medicine = serializers.StringRelatedField(read_only=True)
    patient = SimplePatientSerializer(source='prescription.patient', read_only=True)

    class Meta:
        model = PrescriptionMedicines
        fields = ['medicine', 'patient', 'dosage', 'fraction', 'days', 'period', 'description']


class RetrievePrescriptionSerializer(serializers.ModelSerializer):
    doctor = SimpleDoctorSerializer(read_only=True)
    patient = SimplePatientSerializer(read_only=True)
    medicines = RetrievePrescriptionMedicinesSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'doctor', 'patient', 'description', 'date_time', 'medicines']


class ListPrescriptionsFilteredByDoctorPatientSerializer(serializers.ModelSerializer):
    medicines_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'date_time', 'medicines_count']


class ListPrescriptionsMedicinesFilteredByDoctorPatientSerializer(serializers.ModelSerializer):
    medicine = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PrescriptionMedicines
        fields = ['id', 'medicine', 'dosage', 'fraction', 'days', 'start']


# TODO: POST Prescription & Its Medicines In ONE NESTED JSON & ONE STEP
# class POSTPrescriptionSerializer(serializers.Serializer):
#     pass

# _______________________________________________________________________________________


class ListDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id','first_name', 'last_name', 'profile_pic', 'field']


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

    def create(self, validated_data):
        doctor = Doctor.objects.create(
            **validated_data, role='D'
        )
        doctor.save()

        return doctor


class RetriveDoctorSerializer(serializers.ModelSerializer):
    prescription_date = serializers.SerializerMethodField('get_prescription_date')
    prescriptions_num = serializers.SerializerMethodField('get_prescriptions_num')
    medicines_num = serializers.SerializerMethodField('get_medicines_num')

    def get_prescription_date(self, doctor):
        return self.context.get("prescription_date")

    def get_prescriptions_num(self, doctor):
        return self.context.get("prescriptions_num")

    def get_medicines_num(self, doctor):
        return self.context.get("medicines_num")

    class Meta:
        model = Doctor
        fields = (
            'id',
            'first_name',
            'last_name',
            'profile_pic',
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
            'prescription_date',
            'prescriptions_num',
            'medicines_num',

        )
