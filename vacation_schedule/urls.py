from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from . import views

app_name = 'vacation_schedule'
urlpatterns = [
    path('vacation_list/', login_required(views.VacationListPage.as_view()), name='vacationListPage'),
    path('add_vacation/<int:id>/', login_required(views.UpdateOrCreateVacationPeriod.as_view()), name='updateVacation'),
    path('add_vacation/', login_required(views.UpdateOrCreateVacationPeriod.as_view()), name='addVacation'),
    path('delete_vacation/<int:id>/', login_required(views.DeleteVacationPeriod.as_view()), name='deleteVacation'),
    path('employee_vacation/', staff_member_required(views.EmployeeVacationPage.as_view()), name='employeeVacationPage'),
    path('employee_vacation/download/', staff_member_required(views.ExportVacationXlsView.as_view()), name='download'),
]
