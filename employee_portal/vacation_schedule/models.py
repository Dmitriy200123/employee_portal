from django.db import models


# Create your models here.
from employee_information_site.models import Employee


class VacationScheduleParameters(models.Model):
    maxCountDays = models.IntegerField(verbose_name='Максимальное количество дней на отпуск')

    def __str__(self):
        return f'Максимальное количество дней на отпуск: {self.maxCountDays}'


class EmployeeVacationPeriod(models.Model):
    employeeId = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Id сотрудника')
    startDateVacation = models.DateField(verbose_name='Дата начала отпуска')
    endDateVacation = models.DateField(verbose_name='Дата окончания отпуска')
    vacationDays = models.IntegerField(verbose_name='Продолжительность отпуска')

    def __str__(self):
        return f'{self.employeeId}: {self.startDateVacation}-{self.endDateVacation}'
