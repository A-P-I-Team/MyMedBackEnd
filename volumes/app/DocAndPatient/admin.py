from django.contrib import admin
from .models import Doctor,Prescription,PrescriptionMedicines,Medicine
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedicines)
admin.site.register(Medicine)