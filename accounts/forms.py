from django import forms
from .models import AdvUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import user_registrated
from django.forms import ModelForm, TextInput, NumberInput, EmailInput, PasswordInput, CheckboxInput, FileInput
from django.core.validators import MaxValueValidator, MinValueValidator


class ChangeUserinfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Aдpec электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'patronymic', 'last_name', 'image')
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите логин'
            }),
            "email": EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите электронную почту'
            }),
            "first_name": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите ваше имя'
            }),
            "last_name": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите вашу фамилию'
            }),
            "patronymic": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите ваше отчество'
            }),
            "image": FileInput(attrs={
                'class': 'form-control', 'style': 'height: 60px'
            }),
        }


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html(),
                                min_length=8)
    password2 = forms.CharField(label='Пароль повторно', widget=forms.PasswordInput,
                                help_text='Повторите пороль',
                                min_length=8)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', None)
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super(RegisterUserForm, self).clean()
        password1 = self.clean_password1()
        password2 = self.cleaned_data.get('password2', None)
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пороли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_messages', 'image')

        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите логин'
            }),
            "email": EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите электронную почту'
            }),
            "password1": PasswordInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите пароль'
            }),
            "password2": PasswordInput(attrs={
                'class': 'form-control', 'placeholder': 'Повторите пароль'
            }),
            "first_name": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите ваше имя'
            }),
            "last_name": TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите вашу фамилию'
            }),
            "send_messages": CheckboxInput(attrs={
                'class': 'check__input'
            }),
        }