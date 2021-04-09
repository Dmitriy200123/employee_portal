from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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
        return f'{self.department.name}: {self.name}'


class PersonBase(models.Model):
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='employee_photos', default='skb_lab.jpg')
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Employee(PersonBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(CompanyDepartment, null=True, on_delete=models.SET_NULL)
    position = models.ForeignKey(EmployeePosition, null=True, on_delete=models.SET_NULL)
    is_new_employee = models.BooleanField()

    class Meta:
        ordering = ['department', 'position', 'full_name']

    def __str__(self):
        return self.full_name


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
        ordering = ['created_at', 'position', 'full_name']

    def __str__(self):
        return self.full_name
