from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .models import Accounts

class RegisterForm(forms.ModelForm):
   password = forms.CharField(min_length=8, required=True, validators=[
      RegexValidator(regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$', message=['Sandi minimal 8 karakter', 'Terdapat huruf kapital', 'Terdapat simbol (!@#$%^&*)'], code='invalid')
   ], widget=forms.PasswordInput())
   class Meta:
      model = Accounts
      fields = ['username', 'email', 'password']
      error_messages = {
         'username': {'unique': _('Nama pengguna telah digunakan')},
         'email': {'unique': _('Email telah digunakan')},
      }
   
   def save(self, commit = False):
      password = self.cleaned_data['password']
      instance = super().save(commit)
      instance.set_password(password)
      instance.save()
      return instance