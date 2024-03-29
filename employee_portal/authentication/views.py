from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic
from .forms import LoginForm, RegisterForm
from employee_information_site.models import Employee


# Create your views here.

class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('employee_information_site:employee_questionnaire')

    # auto authentication and redirect to profile
    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)


class EmployeeLoginView(LoginView):
    profile_url = reverse_lazy('employee_information_site:profile')
    employee_questionnaire = reverse_lazy('employee_information_site:employee_questionnaire')
    form_class = LoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        employee = Employee.objects.filter(user=self.request.user.id).first()
        if employee is None:
            return redirect(self.employee_questionnaire)
        return redirect(self.profile_url)
