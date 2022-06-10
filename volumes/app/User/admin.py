from django.contrib import admin
from .models import User,City
# Register your models here.


# admin.site.register(User)
# admin.site.register(User,UserAdmin)
admin.site.register(City)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'ssn','gender')
    list_filter = ('gender', 'user_city','isVaccinated')
    search_fields = ['username', 'first_name','last_name']

