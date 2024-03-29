from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

from User.models import User


# Create your models here.
class Doctor(User):
    DEGREE_GENERAL = 'GP'
    DEGREE_SPECIAL = 'SP'
    DEGREE_SUBSPEC = 'SS'
    DEGREE_CHOICES = [
        (DEGREE_GENERAL, 'General Practitioner'),
        (DEGREE_SPECIAL, 'Specialist'),
        (DEGREE_SUBSPEC, 'Sub-Specialist'),
    ]

    FIELD_CARDIOLOGIST = 'CAR'
    FIELD_NEUROLOGIST = 'NEU'
    FIELD_GEYNECOLOGIST = 'GYN'
    FIELD_OBSTETRICIAN = 'OBS'
    FIELD_PEDIATRICIAN = 'PED'
    FIELD_UROLOGISTS = 'URO'
    FIELD_OTOLARYNGOLOGIST = 'OTL'
    FIELD_INFECTION_DISEASE = 'INF'
    FIELD_INTERNAL_MEDICINE = 'INT'
    FIELD_SURGEON = 'SUR'
    FIELD_RADIOLOGIST = 'RAL'
    FIELD_RADIOTHERAPY = 'RAT'
    FIELD_PHYSIOLOGIST = 'PHY'
    FIELD_ORTHOPEDIST = 'ORT'
    FIELD_PATHOLOGY = 'PAT'
    FIELD_CHOICES = [
        (FIELD_CARDIOLOGIST, 'Cardiologist'),
        (FIELD_NEUROLOGIST, 'Neurologist'),
        (FIELD_GEYNECOLOGIST, 'Geynecologist'),
        (FIELD_OBSTETRICIAN, 'Obstetrician'),
        (FIELD_PEDIATRICIAN, 'Pediatrician'),
        (FIELD_UROLOGISTS, 'Urologists'),
        (FIELD_OTOLARYNGOLOGIST, 'Otolaryngologist'),
        (FIELD_INFECTION_DISEASE, 'Infection Disease'),
        (FIELD_INTERNAL_MEDICINE, 'Internal Medicine'),
        (FIELD_SURGEON, 'Surgeon'),
        (FIELD_RADIOLOGIST, 'Radiologist'),
        (FIELD_RADIOTHERAPY, 'Radiotherapy'),
        (FIELD_PHYSIOLOGIST, 'Physiologist'),
        (FIELD_ORTHOPEDIST, 'Orthopedist'),
        (FIELD_PATHOLOGY, 'Pathology'),
    ]

    # role = models.CharField(max_length=1, default='D', choices=[('D', 'Doctor')])
    msn = models.CharField(unique=True, max_length=10, validators=[RegexValidator(regex='^[0-9]{10}$')], null=True,
                           blank=True)
    degree = models.CharField(max_length=2, choices=DEGREE_CHOICES, null=True, blank=True)
    field = models.CharField(max_length=3, choices=FIELD_CHOICES, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    hours_of_work = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(unique=True, max_length=11, validators=[RegexValidator(regex='^[0-9]{11}$')], null=True,
                             blank=True)
    officeno = models.CharField(unique=True, max_length=11, validators=[RegexValidator(regex='^[0-9]{11}$')], null=True,
                                blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# class Patient(models.Model):
#     GENDER_MALE = 'M'
#     GENDER_FEMALE = 'F'
#     GENDER_OTHER = 'O'
#     GENDER_CHOICES = [
#         (GENDER_MALE, 'Male'),
#         (GENDER_FEMALE, 'Female'),
#         (GENDER_OTHER, 'Other'),
#     ]
#
#     INSURANCE_CO1 = 'INS1'
#     INSURANCE_CO2 = 'INS2'
#     INSURANCE_CO3 = 'INS3'
#     INSURANCE_CO4 = 'INS4'
#     INSURANCE_CO_CHOICES = [
#         (INSURANCE_CO1, 'InsuranceCo1'),
#         (INSURANCE_CO2, 'InsuranceCo2'),
#         (INSURANCE_CO3, 'InsuranceCo3'),
#         (INSURANCE_CO4, 'InsuranceCo4'),
#     ]
#
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ssn = models.CharField(unique=True, max_length=10, validators=[RegexValidator(regex='^[0-9]{10}$')])
#     # first_name = models.CharField(max_length=150)
#     # last_name = models.CharField(max_length=150)
#     birthdate = models.DateField()
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     image = models.ImageField(upload_to='patients/profile-images/', null=True, blank=True)
#     phone = models.CharField(unique=True, max_length=11, validators=[RegexValidator(regex='^[0-9]{11}$')])
#     mobile = models.CharField(unique=True, max_length=11, validators=[RegexValidator(regex='^[0-9]{11}$')])
#     insurance_no = models.CharField(unique=True, max_length=10, validators=[RegexValidator(regex='^[0-9]{10}$')])
#     insurance_co = models.CharField(max_length=10, choices=INSURANCE_CO_CHOICES)
#
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'


# class MedicineManufacturer(models.Model):
#     name = models.CharField(max_length=150)
#
#     def __str__(self):
#         return self.name


class Medicine(models.Model):
    TYPE_AMPOULE = 'A'
    TYPE_TABLET = 'T'
    TYPE_SYRUP = 'S'
    TYPE_CHOICES = [
        (TYPE_AMPOULE, 'Ampoule'),
        (TYPE_TABLET, 'Tablet'),
        (TYPE_SYRUP, 'Syrup'),
    ]
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    # manufacturer = models.ForeignKey(MedicineManufacturer, on_delete=models.CASCADE, related_name='medicines')

    def __str__(self):
        # return f'Manufacturer:{self.manufacturer}, Type:{self.type}, {self.name}'
        return f'{self.name}'


class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='prescriptionsofdoctor')
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='prescriptionsofpatient')
    description = models.TextField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Doctor:{self.doctor}, Patient:{self.patient}, DateTime:{self.date_time}'


class PrescriptionMedicines(models.Model):
    FRACTION_4Q = '1'
    FRACTION_3Q = '3/4'
    FRACTION_2Q = '1/2'
    FRACTION_1Q = '1/4'

    FRACTION_CHOICES = [
        (FRACTION_1Q, '1 Quarter'),
        (FRACTION_2Q, '2 Quarter'),
        (FRACTION_3Q, '3 Quarter'),
        (FRACTION_4Q, '4 Quarter')
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name='prescriptions')
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    dosage = models.PositiveSmallIntegerField()
    fraction = models.CharField(max_length=3, default='1', choices=FRACTION_CHOICES)
    days = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(default=1)
    start = models.DateTimeField(null=True, blank=True)
    takenno = models.PositiveSmallIntegerField(default=0)
    nottakenno = models.PositiveSmallIntegerField(default=0)
    # active = models.NullBooleanField(default=None)
    notify = models.BooleanField(default=False)
    # مثلاً: هر ۸ ساعت یک عدد
    description = models.TextField(null=True, blank=True)

    # class Meta:
    #     unique_together = ('medicine', 'prescription')


class Reminder(models.Model):
    prescription_medicine = models.ForeignKey(PrescriptionMedicines, on_delete=models.CASCADE, related_name='reminders')
    date_time = models.DateTimeField()
    status = models.BooleanField(null=True, blank=True, default=None)
