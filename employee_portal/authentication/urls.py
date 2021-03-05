from django.urls import path

from . import views

app_name = 'authentication'
urlpatterns = [
    path('auth', views.CreateView, name='auth'),
]