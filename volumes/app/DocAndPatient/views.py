from django.db.models import Q
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Doctor, Medicine, Prescription, PrescriptionMedicines
from .permissions import IsAdminOrReadOnly, IsDoctorOrReadOnly, IsPrescriptionOwner
from .serializers import ListDoctorSerializer, FullDoctorSerializer, RetriveDoctorSerializer, SimpleDoctorSerializer, \
    MedicineSerializer, PrescriptionSerializer, PrescriptionMedicinesSerializer, \
    RetrievePrescriptionSerializer, ListPrescriptionsFilteredByDoctorPatientSerializer, \
    ListPrescriptionMedicinesSerializer, RetrievePrescriptionMedicinesSerializer, ListPrescriptionsMedicinesFilteredByDoctorPatientSerializer


# Create your views here.
class User_Doctors_List(ListAPIView):
    serializer_class = ListDoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.request.user.prescriptionsofpatient.all()
        queryset2 = []
        for i in queryset:
            queryset2.append(i.doctor)

        return queryset2


class ListCreateDoctor(ListCreateAPIView):
    serializer_class = FullDoctorSerializer
    queryset = Doctor.objects.all()


class RetriveDoctor(RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = RetriveDoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        doctor = None
        doctor = Doctor.objects.filter(id=self.kwargs['pk'])
        if (doctor):
            doctor = doctor.first()
            user = self.request.user
            prescriptions = Prescription.objects.filter(doctor=doctor, patient=user)
            if (prescriptions):
                medicines_num = 0
                for i in prescriptions:
                    medicines = i.medicines.all()
                    medicines_num += len(medicines)

                prescriptions_num = len(prescriptions)
                prescriptions = prescriptions.last()
                return {'prescription_date': prescriptions.date_time, 'prescriptions_num': prescriptions_num,
                        'medicines_num': medicines_num}


            else:
                return {'prescription_date': None, 'prescriptions_num': 0, 'medicines_num': 0}
        else:
            return {'prescription_date': None, 'prescriptions_num': 0, 'medicines_num': 0}

# ================================================================================


class MedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# TODO: POST Prescription & Its Medicines In ONE NESTED JSON & ONE STEP
class PrescriptionViewSet(ModelViewSet):
    # TODO: IsPrescriptionOfOwnerDoctor
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor_id', 'patient_id']
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly, IsPrescriptionOwner]

    # def get_queryset(self):
    #     if self.request.user.role == 'D':
    #         queryset = Prescription.objects.prefetch_related('medicines').filter(doctor=self.request.user.id)
    #         if self.request.query_params.get('patient_id', None):
    #             return queryset.annotate(medicines_count=Count('medicines'))
    #         return queryset
    #     elif self.request.user.role == 'P':
    #         queryset = Prescription.objects.prefetch_related('medicines').filter(patient=self.request.user.id)
    #         if self.request.query_params.get('doctor_id', None):
    #             return queryset.annotate(medicines_count=Count('medicines'))
    #         return queryset
    #     elif self.request.user.is_staff:
    #         return Prescription.objects.prefetch_related('medicines').all()

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Prescription.objects.prefetch_related('medicines').all()
        queryset = Prescription.objects.prefetch_related('medicines').filter(
            Q(patient=self.request.user.id) | Q(doctor=self.request.user.id)
        )
        if self.request.query_params.get('doctor_id', None):
            return queryset.annotate(medicines_count=Count('medicines'))
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' and (self.request.query_params.get('doctor_id', None) or self.request.query_params.get('patient_id', None)):
            return ListPrescriptionsFilteredByDoctorPatientSerializer
        elif self.action == 'retrieve':
            return RetrievePrescriptionSerializer

        return PrescriptionSerializer
        # return PrescriptionSerializer(many=isinstance(self.request.data, list))


class PrescriptionMedicinesViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prescription__doctor_id', 'prescription__patient_id']
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]

    # def get_queryset(self):
    #     if self.request.user.role == 'D':
    #         return PrescriptionMedicines.objects.select_related('prescription').filter(prescription__doctor=self.request.user.id)
    #     elif self.request.user.role == 'P':
    #         return PrescriptionMedicines.objects.select_related('prescription').filter(prescription__patient=self.request.user.id)
    #     elif self.request.user.is_staff:
    #         return PrescriptionMedicines.objects.select_related('prescription').all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return PrescriptionMedicines.objects.select_related('prescription').all()
        queryset = PrescriptionMedicines.objects.select_related('prescription').filter(
            Q(prescription__patient=self.request.user.id) | Q(prescription__doctor=self.request.user.id)
        )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            if self.request.query_params.get('prescription__doctor_id', None) or self.request.query_params.get('prescription__patient_id', None):
                return ListPrescriptionsMedicinesFilteredByDoctorPatientSerializer
            else:
                return ListPrescriptionMedicinesSerializer
        elif self.action == 'retrieve':
            return RetrievePrescriptionMedicinesSerializer

        return PrescriptionMedicinesSerializer
        # return PrescriptionMedicinesSerializer(many=isinstance(self.request.data, list))
