from django import forms
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ProfileForm
from .models import Employee, Service


# Create your views here.


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


class ServiceListView(TemplateView):
    template_name = 'employee_information_site/service_list.html'

    def get(self, request, *args, **kwargs):
        context = {'list': Service.objects.all()}
        return render(request, self.template_name, context)

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
        form.fields['is_new_employee'].disabled = True
