from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, UpdateView, DeleteView

# Create your views here.
from employee_information_site.models import Employee
from vacation_schedule.forms import VacationPeriodForm
from vacation_schedule.models import EmployeeVacationPeriod, DaysRemainder


class VacationListPage(ListView):
    template_name = 'vacation_schedule/vacation_list_page.html'
    model = EmployeeVacationPeriod
    context_object_name = 'vacation_periods'

    def get_queryset(self):
        queryset = super().get_queryset()
        employee = Employee.objects.filter(user=self.request.user.id).first()
        current_year = datetime.now().year

        return queryset.filter(employeeId=employee.id, startDateVacation__year=current_year)

    def get_context_data(self, **kwargs):
        context = super(VacationListPage, self).get_context_data(**kwargs)
        employee = Employee.objects.filter(user=self.request.user.id).first()
        context['days_remainder'] = DaysRemainder.objects.filter(employee=employee).first()
        return context


class UpdateOrCreateVacationPeriod(UpdateView):
    model = EmployeeVacationPeriod
    form_class = VacationPeriodForm
    template_name = 'vacation_schedule/add_vacation_page.html'
    success_url = reverse_lazy('vacation_schedule:vacationListPage')
    context_object_name = 'form'

    def get_object(self, **kwargs):
        vacation_id = self.kwargs.get('id')

        return self.model.objects.filter(id=vacation_id).first()

    def form_invalid(self, form):
        return self.form_validate(form)

    def form_valid(self, form):
        return self.form_validate(form)

    def form_validate(self, form):
        if not form.errors.get('employeeId') is None:
            form.errors.pop('employeeId')

        if not form.errors.get('vacationDays') is None:
            form.errors.pop('vacationDays')

        employee = Employee.objects.filter(user=self.request.user.id).first()
        days_remainder = DaysRemainder.objects.filter(employee=employee).first()

        if form.instance.vacationDays:
            days_remainder.remainder += form.instance.vacationDays

        form.instance.employeeId = employee
        form.instance.vacationDays = (form.instance.endDateVacation - form.instance.startDateVacation).days

        if form.instance.vacationDays <= 0:
            form.add_error('endDateVacation', 'Неправильно выбрана дата окончания отпуска')

        if form.instance.vacationDays > days_remainder.remainder:
            form.add_error('vacationDays', 'Выбрано больше дней, чем осталось')

        if form.is_valid():
            days_remainder.remainder -= form.instance.vacationDays
            days_remainder.save()
            return super().form_valid(form)

        return super().form_invalid(form)


class DeleteVacationPeriod(DeleteView):
    model = EmployeeVacationPeriod
    success_url = reverse_lazy('vacation_schedule:vacationListPage')
    context_object_name = 'period'

    def get_object(self, **kwargs):
        vacation_id = self.kwargs.get('id')

        return get_object_or_404(self.model, id=vacation_id)

    def delete(self, request, *args, **kwargs):
        vacation_period = self.get_object(**kwargs)
        days_remainder = DaysRemainder.objects.filter(employee=vacation_period.employeeId).first()
        days_remainder.remainder += vacation_period.vacationDays

        if days_remainder.remainder > days_remainder.maxCountDays.maxCountDays:
            days_remainder.remainder = days_remainder.maxCountDays.maxCountDays

        days_remainder.save()

        return super(DeleteVacationPeriod, self).delete(request, *args, **kwargs)
