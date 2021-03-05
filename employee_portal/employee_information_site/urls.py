from django.urls import path

from . import views

app_name = 'employee_information_site'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
]