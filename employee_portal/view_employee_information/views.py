from django.views.generic import ListView, TemplateView
from employee_information_site.models import Employee
from view_employee_information.forms import FilterForm


# Create your views here.


class EmployeesListPage(ListView):
    template_name = 'view_employee_information/employees_list_page.html'
    paginate_by = 3
    model = Employee

    def get_queryset(self):
        queryset = super().get_queryset()
        parameters = self.request.GET

        if parameters:
            return self.__filtered_employees(queryset, parameters)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm
        return context

    @staticmethod
    def __filtered_employees(queryset, parameters):
        full_name = 'full_name'
        department = 'department'
        position = 'position'

        if full_name in parameters:
            queryset = queryset.filter(full_name__contains=parameters[full_name])

        if department in parameters and parameters[department].isdigit():
            queryset = queryset.filter(department=int(parameters[department]))

        if position in parameters and parameters[position].isdigit():
            queryset = queryset.filter(position=int(parameters[position]))

        return queryset


class EmployeeInformationPage(TemplateView):
    template_name = 'view_employee_information/employee_information_page.html'

    def get_context_data(self, **kwargs):
        user = 'user'
        employee = None
        parameters = self.request.GET

        if user in parameters and parameters[user].isdigit():
            employee = Employee.objects.filter(user=parameters[user]).first()

        context = super().get_context_data(**kwargs)
        context['employee'] = employee
        return context
