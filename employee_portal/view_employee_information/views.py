from django.shortcuts import render
from django.views.generic import ListView
from employee_information_site.models import Employee


# Create your views here.

class EmployeeInformationPage(ListView):
    template_name = 'view_employee_information/employee_information_page.html'

    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        context = {'employees': employees}
        return render(request, self.template_name, context)
