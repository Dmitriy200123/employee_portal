from django.views.generic import ListView, TemplateView
from employee_information_site.models import Employee
from view_employee_information.forms import FilterForm
from django.db.models import Q
from django.shortcuts import Http404

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
            names = parameters[full_name].split(' ')

            if len(names) == 1:
                queryset = queryset.filter(
                    Q(first_name__icontains=names[0]) | Q(second_name__icontains=names[0]) |
                    Q(patronymic__icontains=names[0])
                )
            elif len(names) == 2:
                queryset = queryset.filter(
                    Q(first_name__icontains=names[0]) & Q(second_name__icontains=names[1]) |
                    Q(first_name__icontains=names[0]) & Q(patronymic__icontains=names[1]) |
                    Q(second_name__icontains=names[0]) & Q(patronymic__icontains=names[1])
                )
            else:
                queryset = queryset.filter(
                    Q(first_name__icontains=names[0]) & Q(second_name__icontains=names[1]) &
                    Q(patronymic__icontains=names[2]))

        if department in parameters and parameters[department].isdigit():
            queryset = queryset.filter(department=int(parameters[department]))

        if position in parameters and parameters[position].isdigit():
            queryset = queryset.filter(position=int(parameters[position]))

        return queryset


class EmployeeInformationPage(TemplateView):
    template_name = 'view_employee_information/employee_information_page.html'

    def get_context_data(self, **kwargs):
        user = 'user'
        parameters = self.request.GET
        if user in parameters and parameters[user].isdigit():
            employee = Employee.objects.filter(user=parameters[user]).first()
            if employee is not None:
                context = super().get_context_data(**kwargs)
                context['employee'] = employee
                context['user'] = Employee.objects.filter(user=self.request.user).first()
                return context
        raise Http404




