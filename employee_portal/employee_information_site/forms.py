from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import Employee, CompanyDepartment, EmployeePosition


class ProfileForm(ModelForm):
    phone_regex = RegexValidator(regex=r'^\+79\d{9}$',
                                 message="Phone number must be entered in the format: '+79112223344'")
    phone_number = forms.CharField(validators=[phone_regex], max_length=12)

    class Meta:
        model = Employee
        fields = ['user', 'photo', 'full_name', 'email', 'phone_number', 'department', 'position', 'description',
                  'is_new_employee']
        widgets = {
            'user': forms.HiddenInput(),
            'photo': forms.ClearableFileInput(attrs={'class': 'edit'}),
            'full_name': forms.TextInput(attrs={'class': 'edit'}),
            'email': forms.EmailInput(attrs={'class': 'edit'}),
            'phone_number': forms.NumberInput(attrs={'class': 'edit'}),
            'department': forms.Select(choices=CompanyDepartment.objects.all(), attrs={'class': 'edit'}),
            'position': forms.Select(choices=EmployeePosition.objects.all(), attrs={'class': 'edit'}),
            'description': forms.Textarea(attrs={'class': 'edit'}),
        }
