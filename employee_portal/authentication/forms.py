from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Логин"),
        widget=forms.TextInput(attrs={'class': 'login'}),
    )
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'password'}),
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label=_("Логин"),
        widget=forms.TextInput(attrs={'class': 'login'}),
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
