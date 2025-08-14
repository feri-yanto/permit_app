from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Accounts


# REGISTER FORM
class RegisterForm(forms.ModelForm):
   password = forms.CharField(min_length=8, required=True, validators=[
      RegexValidator(regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$', message=['Sandi minimal 8 karakter', 'Terdapat huruf kapital', 'Terdapat simbol (!@#$%^&*)'], code='invalid')
   ], widget=forms.PasswordInput())
   
   class Meta:
      model = Accounts
      fields = ['username', 'email', 'password']
      error_messages = {
         'username': {
            'invalid': _('Nama pengguna hanya dapat berupa huruf, angka, dan simbol (@/./+/-/_) tanpa menggunakan spasi'),
            'unique': _('Nama pengguna telah digunakan')
         },
         'email': {'unique': _('Email telah digunakan')},
      }
   
   def save(self, commit = True):
      password = self.cleaned_data['password']
      self.instance.set_password(password)
      return super().save(commit)


# LOGIN FORM
class LoginForm(forms.Form):
   username = forms.CharField(max_length=50, required=True, widget=forms.TextInput())
   password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput())

   def __init__(self, request, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.request = request
      self.__user = None
   
   @property
   def get_user(self):
      return self.__user
   
   def clean(self):
      data = self.cleaned_data
      user = authenticate(self.request, **data)
      if user is None:
         raise ValidationError(message=_('Login gagal, pastikan akun anda telah aktif dan data yang anda masukan benar'), code='login_invalid')
      self.__user = user
      return super().clean()