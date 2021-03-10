from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .forms import ProfileForm
from .models import Employee


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


class ProfileEditPageView(TemplateView):
    template_name = 'employee_information_site/profile_edit.html'

    def get(self, request, *args, **kwargs):
        employee = Employee.objects.filter(user=request.user.id)
        if employee:
            form = ProfileForm(instance=employee.first())
        else:
            form = ProfileForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        employee = Employee.objects.filter(user=request.user.id)
        if employee:
            form = ProfileForm(request.POST, request.FILES, initial={'user': request.user.id},
                               instance=employee.first())
        else:
            form = ProfileForm(request.POST, request.FILES, initial={'user': request.user.id})
        form.fields['user'].disabled = True
        if form.is_valid():
            form.save()
            return redirect('employee_information_site:profile')

        return render(request, self.template_name, {'form': form})
