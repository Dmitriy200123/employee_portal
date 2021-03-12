from django import forms
from django.forms import ModelForm
from .models import Employee


class ProfileForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'photo', 'full_name', 'email', 'phone_number', 'department', 'position', 'is_new_employee']
        widgets = {'user': forms.HiddenInput()}
