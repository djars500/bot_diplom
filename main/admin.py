from django.contrib import admin
from .models import MedicalCenter, Employee, RegisterRequest, Special, City

# Register your models here.

admin.site.register(MedicalCenter)
admin.site.register(Employee)
admin.site.register(RegisterRequest)
admin.site.register(Special)
admin.site.register(City)