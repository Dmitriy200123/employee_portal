from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'employee_information_site'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('profile/', login_required(views.ProfilePageView.as_view()), name='profile'),
    path('profile_edit/', login_required(views.ProfileEditPageView.as_view()), name="profile_edit")
]
