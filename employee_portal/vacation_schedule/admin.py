from django.contrib import admin

# Register your models here.
from vacation_schedule.models import VacationScheduleParameters, EmployeeVacationPeriod, DaysRemainder

admin.site.register(VacationScheduleParameters)
admin.site.register(EmployeeVacationPeriod)
admin.site.register(DaysRemainder)
