from django.contrib import admin
from .models import Candidate, CompanyDepartment, EmployeePosition, Employee

# Register your models here.


class CandidateList(admin.ModelAdmin):
    list_display = ('fullName', 'entryDate', 'position')
    list_filter = ['entryDate', 'position']
    search_fields = ['fullName']


admin.site.register(Candidate, CandidateList)
admin.site.register(CompanyDepartment)
admin.site.register(EmployeePosition)
admin.site.register(Employee)