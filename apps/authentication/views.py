from django.views.generic import CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Accounts
from .forms import RegisterForm
from .tokens import generate_token
from .mail import send_mail_confirmation

# VIEW FOR REGISTER NEW USER
class RegisterUserView(SuccessMessageMixin, CreateView):
   http_method_names = ['get', 'post']
   template_name = 'auth/register.html'
   model = Accounts
   form_class = RegisterForm
   success_url = reverse_lazy('auth:login')
   success_message = 'Akun berhasil dibuat'