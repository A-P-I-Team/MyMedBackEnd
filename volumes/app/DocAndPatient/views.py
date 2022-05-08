from django.shortcuts import render
from requests import request
from rest_framework.generics import *
from .serializers import ListDoctorSerializer,FullDoctorSerializer,RetriveDoctorSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Doctor,Prescription

# Create your views here.
class User_Doctors_List(ListAPIView):
    serializer_class=ListDoctorSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = self.request.user.prescriptionsofpatient.all()
        queryset2=[]
        for i in queryset:
            queryset2.append(i.doctor)
        
        return queryset2
    

class ListCreateDoctor(ListCreateAPIView):
    serializer_class=FullDoctorSerializer
    queryset= Doctor.objects.all()



class RetriveDoctor(RetrieveAPIView):
    queryset=Doctor.objects.all()
    serializer_class=RetriveDoctorSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        doctor=None
        doctor = Doctor.objects.filter(id=self.kwargs['pk'])
        if(doctor):
            doctor=doctor.first()
            user = self.request.user
            prescriptions=Prescription.objects.filter(doctor=doctor,patient=user)
            if(prescriptions):
                medicines_num = 0
                for i in prescriptions:
                    medicines = i.medicines.all()
                    medicines_num += len(medicines)


                prescriptions_num = len(prescriptions)
                prescriptions=prescriptions.last()
                return {'prescription_date' : prescriptions.date_time ,'prescriptions_num' : prescriptions_num ,'medicines_num' : medicines_num}


            else:
                 return {'prescription_date' : None ,'prescriptions_num' : 0 ,'medicines_num' : 0}
        else:
             return {'prescription_date' : None ,'prescriptions_num' : 0 ,'medicines_num' : 0}
