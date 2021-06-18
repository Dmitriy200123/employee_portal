from django.contrib import admin
from .models import CompanyDepartment, EmployeePosition, Employee, Candidate, CandidateProspectivePosition, Service, \
    EmployeeServices


# Register your models here.


class EmployeeList(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'patronymic', 'created_at', 'position')
    list_filter = ['created_at', 'position']
    search_fields = ['first_name', 'second_name', 'patronymic']


class CandidateList(EmployeeList):
    list_filter = ['position', 'created_at', 'updated_at']


admin.site.register(CompanyDepartment)

admin.site.register(EmployeePosition)
admin.site.register(Employee, EmployeeList)

admin.site.register(CandidateProspectivePosition)
admin.site.register(Candidate, CandidateList)

admin.site.register(Service)
admin.site.register(EmployeeServices)

admin.site.site_title = 'Корпоративный портал SKB-LAB'
admin.site.site_header = 'Корпоративный портал SKB-LAB'