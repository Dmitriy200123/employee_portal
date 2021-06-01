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
            'startDateVacation': forms.SelectDateWidget(years=range(current_year, current_year + 1)),
            'endDateVacation': forms.SelectDateWidget(years=range(current_year, current_year + 1))
        }
