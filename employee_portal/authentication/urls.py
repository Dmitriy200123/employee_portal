from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'authentication'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login',),
    path('logout/', views.LogoutView.as_view(), name='logout')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)