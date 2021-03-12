from django.contrib import admin
from .models import CompanyDepartment, EmployeePosition, Employee


# Register your models here.


class EmployeeList(admin.ModelAdmin):
    list_display = ('full_name', 'created_at', 'position')
    list_filter = ['created_at', 'position']
    search_fields = ['full_name']


admin.site.register(CompanyDepartment)
admin.site.register(EmployeePosition)
admin.site.register(Employee, EmployeeList)
