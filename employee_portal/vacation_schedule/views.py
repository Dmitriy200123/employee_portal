# Create your views here.
from django.views.generic import ListView, TemplateView


class VacationListPage(TemplateView):
    template_name = 'vacation_schedule/vacation_list_page.html'
