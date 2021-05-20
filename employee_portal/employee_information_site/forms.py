from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import Employee, CompanyDepartment, EmployeePosition


class ProfileForm(ModelForm):
    phone_regex = RegexValidator(regex=r'^\+79\d{9}$',
                                 message="Phone number must be entered in the format: '+79112223344'")
    phone_number = forms.CharField(validators=[phone_regex], max_length=12, widget=forms.TextInput(attrs={'class': 'edit'}))

    class Meta:
        model = Employee
        fields = ['user', 'photo', 'first_name', 'second_name', 'patronymic', 'email', 'phone_number', 'department', 'position', 'description',
                  'is_new_employee']
        widgets = {
            'user': forms.HiddenInput(),
            'photo': forms.ClearableFileInput(attrs={'class': 'photo'}),
            'first_name': forms.TextInput(attrs={'class': 'first_name', 'placeholder': 'Введите имя'}),
            'second_name': forms.TextInput(attrs={'class': 'second_name', 'placeholder': 'Введите фамилию'}),
            'patronymic': forms.TextInput(attrs={'class': 'patronymic', 'placeholder': 'Введите отчество'}),
            'email': forms.EmailInput(attrs={'class': 'email', 'placeholder': 'userr@gmail.com'}),
            'department': forms.Select(choices=CompanyDepartment.objects.all(), attrs={'class': 'department', 'placeholder': 'Выберите отдел'}),
            'position': forms.Select(choices=EmployeePosition.objects.all(), attrs={'class': 'position', 'placeholder': 'Выберите должность'}),
            'description': forms.Textarea(attrs={'class': 'description', 'placeholder': 'Напишите что-нибудь о себе'}),
        }
