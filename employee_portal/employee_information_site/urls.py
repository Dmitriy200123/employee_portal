from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'employee_information_site'
urlpatterns = [
    path('', views.HomeRedirectView.as_view(), name='home_page'),
    path('employee_questionnaire/', views.EmployeeQuestionnaire.as_view(), name='employee_questionnaire'),
    path('profile/', login_required(views.ProfilePageView.as_view()), name='profile'),
    path('profile_edit/', login_required(views.ProfileEditPageView.as_view()), name="profile_edit"),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('positions/<int:department>/', login_required(views.PositionView.as_view()), name='position'),
]
