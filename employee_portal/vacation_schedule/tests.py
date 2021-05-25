from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from employee_information_site.models import Employee
from vacation_schedule.models import VacationScheduleParameters, DaysRemainder, EmployeeVacationPeriod
from vacation_schedule.recalculating import deleteVacationPeriodsByYear
from vacation_schedule.views import VacationListPage
from view_employee_information.tests import MainTest


# Create your tests here.

def create_parameters():
    parameters = VacationScheduleParameters.objects.get_or_create(maxCountDays=30)[0]
    parameters.save()

    return parameters


def create_days_remainder(employee, parameters):
    days_remainder = DaysRemainder.objects.get_or_create(employee=employee, maxCountDays=parameters)[0]
    days_remainder.save()

    return days_remainder


def create_vacation(employee, year, month, day):
    days_remainder = create_days_remainder(employee, create_parameters())

    start_date = datetime(year, month, day)
    end_date = datetime(year, month, day + 10)
    vacation_days = (end_date - start_date).days

    vacation = EmployeeVacationPeriod.objects.get_or_create(employeeId=employee, startDateVacation=start_date,
                                                            endDateVacation=end_date,
                                                            vacationDays=vacation_days)[0]
    vacation.save()

    days_remainder.remainder -= vacation.vacationDays
    days_remainder.save()

    context = {'days_remainder': days_remainder, 'vacation': vacation}
    return context


class ClientTest(MainTest):
    def setUp(self):
        super(ClientTest, self).setUp()

        user = User.objects.get(username='test')
        self.employee = Employee.objects.get(user=user)
        self.client = Client()
        self.client._login(user)


class DeleteTest(MainTest):
    def setUp(self):
        super(DeleteTest, self).setUp()

        user = User.objects.get(username='test')
        employee = Employee.objects.get(user=user)
        self.year = 2021
        self.month = 5
        self.day = 10

        context = create_vacation(employee, self.year, self.month, self.day)

        self.days_remainder = context['days_remainder']

    def test_delete_vacation_should_empty(self):
        deleteVacationPeriodsByYear(self.days_remainder.employee, self.year)

        vacations = EmployeeVacationPeriod.objects.filter(employeeId=self.days_remainder.employee,
                                                          startDateVacation__year=self.year)
        self.assertFalse(vacations)


class VacationPageTest(ClientTest):
    def test_vacation_list_should_empty(self):
        response = self.client.get(reverse_lazy('vacation_schedule:vacationListPage'))

        vacations = response.context_data[VacationListPage.context_object_name]

        self.assertFalse(vacations)

    def test_vacation_list_should_not_empty(self):
        create_vacation(self.employee, 2021, 5, 10)

        self.client.get(reverse_lazy('vacation_schedule:vacationListPage'))

        response = self.client.get(reverse_lazy('vacation_schedule:vacationListPage'))
        vacations = response.context_data[VacationListPage.context_object_name]

        self.assertTrue(vacations)

    def test_vacation_list_should_contains(self):
        context = create_vacation(self.employee, 2021, 5, 10)

        self.client.get(reverse_lazy('vacation_schedule:vacationListPage'))

        response = self.client.get(reverse_lazy('vacation_schedule:vacationListPage'))
        vacations = response.context_data[VacationListPage.context_object_name]

        self.assertTrue(context['vacation'] in vacations)


class VacationPeriodFormTest(ClientTest):
    @staticmethod
    def create_data(start_day, start_month, start_year, end_day, end_month, end_year):
        start_date = datetime(start_year, start_month, start_day)
        end_date = datetime(end_year, end_month, end_day)

        data = {'startDateVacation_month': start_date.month, 'startDateVacation_day': start_date.day,
                'startDateVacation_year': start_date.year, 'endDateVacation_month': end_date.month,
                'endDateVacation_day': end_date.day, 'endDateVacation_year': end_date.year}

        return data

    def test_form_should_empty(self):
        response = self.client.get(reverse_lazy('vacation_schedule:addVacation'))
        instance = response.context_data['form'].instance
        self.assertIsNone(instance.id)

    def test_form_should_create_vacation(self):
        create_days_remainder(self.employee, create_parameters())
        data = self.create_data(10, 5, 2021, 20, 5, 2021)

        response = self.client.post(reverse_lazy('vacation_schedule:addVacation'), data=data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_form_should_not_empty(self):
        create_days_remainder(self.employee, create_parameters())
        data = self.create_data(9, 5, 2021, 18, 5, 2021)

        self.client.post(reverse_lazy('vacation_schedule:addVacation'), data=data)

        vacation = EmployeeVacationPeriod.objects.first()
        response = self.client.get(reverse_lazy('vacation_schedule:updateVacation', kwargs={'id': vacation.id}))
        instance = response.context_data['form'].instance

        self.assertEquals(instance.id, vacation.id)

    def test_form_should_error(self):
        create_days_remainder(self.employee, create_parameters())
        data = self.create_data(10, 5, 2021, 5, 5, 2021)

        response = self.client.post(reverse_lazy('vacation_schedule:addVacation'), data=data)

        self.assertContains(response, '<li>Неправильно выбрана дата окончания отпуска</li>')
