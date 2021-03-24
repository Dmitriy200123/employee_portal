from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', login_required(views.EmployeesListPage.as_view()), name='employeesListInformation'),
    path('employee/', login_required(views.EmployeeInformationPage.as_view()), name='employeeInformation'),
]
