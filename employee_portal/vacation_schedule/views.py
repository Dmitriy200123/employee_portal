import xlwt
from django.shortcuts import get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, TemplateView
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
    context_object_name = 'vacation_period'

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

        self.validate_date(form, days_remainder)

        if form.is_valid():
            days_remainder.remainder -= form.instance.vacationDays
            days_remainder.save()
            return super().form_valid(form)

        return super().form_invalid(form)

    def validate_date(self, form, days_remainder):
        if form.instance.vacationDays <= 0:
            form.add_error('endDateVacation', 'Неправильно выбрана дата окончания отпуска')

        if form.instance.vacationDays > days_remainder.remainder:
            form.add_error('vacationDays', 'Выбрано больше дней, чем осталось')

        vacation_periods = self.model.objects.filter(employeeId=days_remainder.employee)

        if vacation_periods:
            if any(x for x in vacation_periods if self.check_date_intersection(form, x)):
                form.add_error('startDateVacation',
                               'Период отпуска пересекается с предыдущими периодамами')

    def get_context_data(self, **kwargs):
        context = super(UpdateOrCreateVacationPeriod, self).get_context_data(**kwargs)
        current_user = Employee.objects.filter(user=self.request.user.id).first()
        context['current_user'] = current_user
        return context

    @staticmethod
    def check_date_intersection(form, vacation_period):
        return form.instance.id != vacation_period.id and (
                vacation_period.startDateVacation <= form.instance.startDateVacation <= vacation_period.endDateVacation
                or vacation_period.startDateVacation <= form.instance.endDateVacation <= vacation_period.endDateVacation
                or form.instance.startDateVacation <= vacation_period.startDateVacation <= form.instance.endDateVacation
                or form.instance.startDateVacation <= vacation_period.endDateVacation <= form.instance.endDateVacation)


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


class EmployeeVacationPage(TemplateView):
    template_name = 'vacation_schedule/employee_vacation_page.html'


class ExportVacationXlsView(DetailView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        row_num = 0

        columns = [field.name for field in EmployeeVacationPeriod._meta.get_fields()][1:]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])

        rows = EmployeeVacationPeriod.objects.all()
        for row_object in rows:
            row_num += 1
            for col_num, value in enumerate(columns):
                ws.write(row_num, col_num, str(getattr(row_object, value)))

        wb.save(response)
        return response
