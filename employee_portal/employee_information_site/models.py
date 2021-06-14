from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class CompanyDepartment(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class EmployeePosition(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(CompanyDepartment, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class PersonBase(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    second_name = models.CharField(max_length=50, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
    photo = models.ImageField(upload_to='employee_photos', default='skb_lab.jpg', verbose_name='Фотография')
    email = models.EmailField(verbose_name='E-mail')
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Employee(PersonBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(CompanyDepartment, null=True, on_delete=models.SET_NULL, verbose_name='Отдел')
    position = models.ForeignKey(EmployeePosition, null=True, on_delete=models.SET_NULL, verbose_name='Должность')
    is_new_employee = models.BooleanField(verbose_name='Я новый сотрудник')

    class Meta:
        ordering = ['department', 'position', 'first_name', 'second_name', 'patronymic']

    def __str__(self):
        return f'{self.first_name} {self.second_name} {self.patronymic}'


class CandidateProspectivePosition(models.Model):
    name = models.CharField(max_length=50, verbose_name='Perspective position')

    def __str__(self):
        return self.name


class Candidate(PersonBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey(CandidateProspectivePosition, null=True, on_delete=models.SET_NULL)
    personal_qualities = models.TextField(blank=True)
    professional_skill = models.TextField(blank=True)
    professional_achievements = models.TextField(blank=True)

    class Meta:
        ordering = ['created_at', 'position', 'first_name', 'second_name', 'patronymic']

    def __str__(self):
        return f'{self.first_name} {self.second_name} {self.patronymic}'


class Service(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class EmployeeServices(models.Model):
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee}:{self.service}"
