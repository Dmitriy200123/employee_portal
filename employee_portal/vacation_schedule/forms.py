from django import forms
from django.utils.datetime_safe import datetime
from vacation_schedule.models import EmployeeVacationPeriod


class VacationPeriodForm(forms.ModelForm):
    class Meta:
        model = EmployeeVacationPeriod
        fields = ['employeeId', 'startDateVacation', 'endDateVacation', 'vacationDays']

        current_year = datetime.now().year

        widgets = {
            'employeeId': forms.HiddenInput,
            'vacationDays': forms.HiddenInput,
            'startDateVacation': forms.DateInput(attrs={'type': 'date', 'class': 'vacation_date start_date'}),
            'endDateVacation': forms.DateInput(attrs={'type': 'date', 'class': 'vacation_date end_date'})
        }
