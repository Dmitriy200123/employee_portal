from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Логин"),
        widget=forms.TextInput(attrs={'class': 'login', 'placeholder': 'username'}),
    )
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'password', 'placeholder': '*********'}),
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label=_("Логин"),
        widget=forms.TextInput(attrs={'class': 'login', 'placeholder': 'username'}),
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'password1', 'placeholder': '*********'}),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'password2', 'placeholder': '*********'}),
        strip=False,
    )
