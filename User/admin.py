from django.contrib import admin
from .models import User,Question,City
# Register your models here.


admin.site.register(User)
# admin.site.register(User,UserAdmin)
admin.site.register(Question)
admin.site.register(City)