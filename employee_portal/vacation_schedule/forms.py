from django import forms
from vacation_schedule.models import EmployeeVacationPeriod


class VacationPeriodForm(forms.ModelForm):
    class Meta:
        model = EmployeeVacationPeriod
        fields = ['employeeId', 'startDateVacation', 'endDateVacation', 'vacationDays']
        widgets = {
            'employeeId': forms.HiddenInput,
            'vacationDays': forms.HiddenInput
        }
