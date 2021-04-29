from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from . import apps

app_name = apps.VacationScheduleConfig.name
urlpatterns = [
    path('vacation_list/', login_required(views.VacationListPage.as_view()), name='vacationListPage'),

]
