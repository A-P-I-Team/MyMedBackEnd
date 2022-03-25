from django.contrib import admin
from .models import User,City
# Register your models here.


admin.site.register(User)
# admin.site.register(User,UserAdmin)
admin.site.register(City)