from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm

from .models import Employee, CompanyDepartment, EmployeePosition


class ProfileForm(ModelForm):
    phone_regex = RegexValidator(regex=r'^\+79\d{9}$',
                                 message="Phone number must be entered in the format: '+79112223344'")
    phone_number = forms.CharField(label='Телефон', validators=[phone_regex], max_length=12,
                                   widget=forms.TextInput(attrs={'class': 'num', 'placeholder': '+7 (999) 999-99-99'}))

    class Meta:
        model = Employee
        fields = ['user', 'photo', 'first_name', 'second_name', 'patronymic', 'email', 'phone_number', 'department',
                  'position', 'description',
                  'is_new_employee']
        widgets = {
            'user': forms.HiddenInput(),
            'photo': forms.ClearableFileInput(attrs={'class': 'photo'}),
            'first_name': forms.TextInput(attrs={'class': 'name', 'placeholder': 'Введите имя'}),
            'second_name': forms.TextInput(attrs={'class': 'name', 'placeholder': 'Введите фамилию'}),
            'patronymic': forms.TextInput(attrs={'class': 'name', 'placeholder': 'Введите отчество'}),
            'email': forms.EmailInput(attrs={'class': 'email', 'placeholder': 'userr@gmail.com'}),
            'department': forms.Select(choices=CompanyDepartment.objects.all(),
                                       attrs={'class': 'department'}),
            'position': forms.Select(choices=EmployeePosition.objects.all(),
                                     attrs={'class': 'position'}),
            'description': forms.Textarea(attrs={'class': 'description', 'placeholder': 'Напишите что-нибудь о себе'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['department'].empty_label = 'Выберите отдел'
        self.fields['position'].empty_label = 'Выберите должность'
