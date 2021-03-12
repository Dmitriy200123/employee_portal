from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class CompanyDepartment(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class EmployeePosition(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(CompanyDepartment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.department.name}: {self.name}'


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='employee_photos')
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)
    department = models.ForeignKey(CompanyDepartment, null=True, on_delete=models.SET_NULL)
    position = models.ForeignKey(EmployeePosition, null=True, on_delete=models.SET_NULL)
    is_new_employee = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
