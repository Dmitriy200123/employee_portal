from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'employee_information_site/home_page.html'
