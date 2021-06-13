from django import forms
from django.forms import ModelForm
from employee_information_site.models import CompanyDepartment, EmployeePosition, Employee


class FilterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['department'].empty_label = 'Выберите отдел'
        self.fields['position'].empty_label = 'Выберите должность'

    department = forms.ModelChoiceField(CompanyDepartment.objects, required=False,
                                        widget=forms.Select(attrs={'class': 'search_parameter department'}))
    position = forms.ModelChoiceField(EmployeePosition.objects, required=False,
                                      widget=forms.Select(choices=EmployeePosition.objects.all(),
                                                          attrs={'class': 'search_parameter position'}))

    class Meta:
        model = Employee
        fields = ['department', 'position']
