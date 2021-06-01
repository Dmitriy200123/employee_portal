import sys
import os
import django

sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'employee_portal.settings'
django.setup()

from django.utils.datetime_safe import datetime
from vacation_schedule.models import VacationScheduleParameters, DaysRemainder, EmployeeVacationPeriod


def deleteVacationPeriodsByYear(employee, year):
    vacation_periods = EmployeeVacationPeriod.objects.filter(employeeId=employee,
                                                             startDateVacation__year=year)
    if vacation_periods:
        [vacation_period.delete() for vacation_period in vacation_periods]


def recalculationDaysRemainderForNewMax():
    new_max_days = int(input('Введите новое число дней на отпуск: '))
    schedule_parameters = VacationScheduleParameters.objects.first()
    current_max_days = schedule_parameters.maxCountDays
    difference = new_max_days - current_max_days

    schedule_parameters.maxCountDays = new_max_days
    schedule_parameters.save()

    for days_remainder in DaysRemainder.objects.all():
        if difference < 0:
            days_remainder.remainder = current_max_days
            deleteVacationPeriodsByYear(days_remainder.employee, datetime.now().year)

        days_remainder.remainder += difference
        days_remainder.save()

    print('Перерасчет завершен')


def resetDaysRemainderForNewYear():
    text_year = input('Введите год или оставьте пустым (будет выбран текущий год): ')
    year = 1981

    if text_year == '':
        year = datetime.now().year
    else:
        year = int(year)

    for days_remainder in DaysRemainder.objects.all():
        deleteVacationPeriodsByYear(days_remainder.employee, year)
        days_remainder.remainder = days_remainder.maxCountDays.maxCountDays
        days_remainder.save()

    print('Перерасчет завершен')


def main():
    print('Выберите действие:\n'
          '1. Установить новое максимальное количество дней на отпуск.\n'
          '2. Сбросить количество дней на отпуск у сотрудников за год\n'
          '3. Выйти')
    action = input()

    if action == '1':
        recalculationDaysRemainderForNewMax()
    elif action == '2':
        resetDaysRemainderForNewYear()
    else:
        return


if __name__ == '__main__':
    main()
