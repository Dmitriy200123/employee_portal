from django import forms
from django.forms import ModelForm
from employee_information_site.models import CompanyDepartment, EmployeePosition, Employee


class FilterForm(ModelForm):
    department = forms.ModelChoiceField(CompanyDepartment.objects, required=False)
    position = forms.ModelChoiceField(EmployeePosition.objects, required=False)

    class Meta:
        model = Employee
        fields = ['department', 'position']
