from datetime import datetime

from django import forms
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from telegram_bot.bot import TelegramBot

from .forms import ProfileForm
from .models import Employee, Service
from chat_bots.models import Sender

# Create your views here.

sender = Sender.objects.first()
chat_bot = sender.newEmployeeChatBot
bot = None
if chat_bot.botType.messenger_type == 'Telegram':
    bot = TelegramBot(chat_bot.token)


class HomePageView(TemplateView):
    template_name = 'employee_information_site/home_page.html'


class ProfilePageView(TemplateView):
    template_name = 'employee_information_site/profile.html'

    def get(self, request, *args, **kwargs):
        employee = Employee.objects.filter(user=request.user.id)

        if not employee:
            return redirect('employee_information_site:profile_edit')

        context = {'employee': employee.first()}
        return render(request, self.template_name, context)


class ServiceListView(ListView):
    template_name = 'employee_information_site/service_list.html'
    model = Service

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {'text': 'Ok'})


class ProfileEditPageView(TemplateView):
    template_name = 'employee_information_site/profile_edit.html'

    def get(self, request, *args, **kwargs):
        employee = Employee.objects.filter(user=request.user.id)

        if employee:
            form = ProfileForm(instance=employee.first())
            form.fields['is_new_employee'].widget = forms.HiddenInput()
        else:
            form = ProfileForm()

        context = {'form': form}
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
            if form.cleaned_data['is_new_employee']:
                data = form.cleaned_data
                message = f"Новый сотрудник {data['full_name']}. Отдел {data['department']}," \
                          f" должность {data['position']}"
                time = f'{datetime.now().date()} {sender.sendTime}'
                bot.post_scheduled_message(time, sender.newEmployeeChannelId, message)

                return redirect('employee_information_site:profile')

        return render(request, self.template_name, {'form': form})

    @staticmethod
    def __disableFields(form: ProfileForm):
        form.fields['user'].disabled = True
        # form.fields['is_new_employee'].disabled = True


class EmployeeQuestionnaire(TemplateView):
    template_name = "employee_information_site/employee_questionnaire.html"

    def get(self, request, *args, **kwargs):
        form = ProfileForm(initial={'user': request.user.id})
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        employee = Employee.objects.filter(user=request.user.id)
        form = ProfileForm(request.POST, request.FILES, initial={'user': request.user.id})

        if form.is_valid():
            form.save()
            return redirect('employee_information_site:profile')

        return render(request, self.template_name, {'form': form})
