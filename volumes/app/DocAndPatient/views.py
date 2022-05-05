from django.shortcuts import render
from requests import request
from rest_framework.generics import *
from .serializers import ListDoctorSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.
class User_Doctors_List(ListCreateAPIView):
    serializer_class=ListDoctorSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = self.request.user.prescriptionsofpatient.doctor.all()
        return queryset
    
    