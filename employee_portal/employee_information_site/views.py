from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, RedirectView
from vacation_schedule.models import DaysRemainder, VacationScheduleParameters

from .forms import ProfileForm
from .models import Employee, Service, EmployeeServices
from chat_bots.sender_bots import SenderBots


# Create your views here.


class HomeRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('authentication:login'))
        elif Employee.objects.filter(user=request.user).first():
            return redirect(reverse_lazy('employee_information_site:profile'))
        else:
            return redirect(reverse_lazy('employee_information_site:employee_questionnaire'))


class ProfilePageView(TemplateView):
    template_name = 'employee_information_site/profile.html'

    def get(self, request, *args, **kwargs):
        current_user = Employee.objects.filter(user=request.user.id)

        if not current_user:
            return redirect('employee_information_site:profile_edit')

        context = {'current_user': current_user.first()}
        return render(request, self.template_name, context)


class ServiceListView(ListView):
    template_name = 'employee_information_site/service_list.html'
    model = Service

    def post(self, request, *args, **kwargs):
        user = Employee.objects.filter(user=request.user.id)
        if not user:
            return redirect('employee_information_site:service_list')

        EmployeeServices.objects.filter(employee=user.first()).delete()

        services = request.POST.getlist('serviceCheck')
        SenderBots.sendAccessEmployeeMessage(user.first(), services)
        for serv in services:
            service = Service.objects.filter(name=serv).first()
            EmployeeServices.objects.update_or_create(employee=user.first(), service=service)
        return render(request, self.template_name, {'text': 'Запрос на доступ отправлен'})

    def get_context_data(self, **kwargs):
        context = super(ServiceListView, self).get_context_data(**kwargs)
        employee = Employee.objects.filter(user=self.request.user.id).first()
        context['current_user'] = employee
        return context


class ProfileEditPageView(TemplateView):
    template_name = 'employee_information_site/profile_edit.html'

    def get(self, request, *args, **kwargs):
        employee = Employee.objects.filter(user=request.user.id)

        if employee:
            form = ProfileForm(instance=employee.first())
            form.fields['is_new_employee'].widget = forms.HiddenInput()
        else:
            form = ProfileForm()

        context = {'form': form, 'current_user': employee.first()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        employee = Employee.objects.filter(user=request.user.id)

        if employee:
            form = ProfileForm(request.POST, request.FILES, instance=employee.first())
            form.fields['is_new_employee'].disabled = True
        else:
            form = ProfileForm(request.POST, request.FILES, initial={'user': request.user.id})

        self.__disableFields(form)

        if form.is_valid():
            form.save()

            return redirect('employee_information_site:profile')

        return render(request, self.template_name, {'form': form})

    @staticmethod
    def __disableFields(form: ProfileForm):
        form.fields['user'].disabled = True


class EmployeeQuestionnaire(TemplateView):
    template_name = "employee_information_site/employee_questionnaire.html"

    def get(self, request, *args, **kwargs):
        form = ProfileForm(initial={'user': request.user.id})
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES, initial={'user': request.user.id})
        form.fields['user'].disabled = True
        if form.is_valid():
            form.save()

            if not DaysRemainder.objects.filter(employee=form.instance):
                days_remainder = DaysRemainder()
                days_remainder.maxCountDays = VacationScheduleParameters.objects.first()
                days_remainder.employee = form.instance
                days_remainder.save()

            if form.cleaned_data['is_new_employee']:
                SenderBots.sendNewEmployeeMessage(form.cleaned_data)
            return redirect('employee_information_site:profile')

        return render(request, self.template_name, {'form': form})
