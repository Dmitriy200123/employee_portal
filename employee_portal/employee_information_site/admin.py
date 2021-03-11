from django.contrib import admin
from .models import CompanyDepartment, EmployeePosition, Employee

# Register your models here.
admin.site.register(CompanyDepartment)
admin.site.register(EmployeePosition)
admin.site.register(Employee)