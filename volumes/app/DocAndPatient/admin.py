from django.contrib import admin
from .models import Doctor, Medicine, Prescription, PrescriptionMedicines, Reminder

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedicines)
admin.site.register(Medicine)
admin.site.register(Reminder)
