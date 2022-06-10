from django.contrib import admin
from .models import Doctor, Medicine, Prescription, PrescriptionMedicines, Reminder

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedicines)
admin.site.register(Medicine)
admin.site.register(Reminder)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'ssn','gender','msn')
    list_filter = ('gender', 'user_city','isVaccinated','degree','field',)
    search_fields = ['username', 'first_name','last_name','about']
