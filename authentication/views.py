from django.views.generic import CreateView, FormView
from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from .models import Accounts
from .forms import RegisterForm, LoginForm
from .tokens import generate_token
from .mail import send_mail_confirmation

# VIEW FOR REGISTER NEW USER
class RegisterUserView(CreateView):
   http_method_names = ['get', 'post']
   template_name = 'auth/register.html'
   model = Accounts
   form_class = RegisterForm
   
   def get_success_url(self):
      user = self.object
      slug = user.slug
      token = generate_token.make_token(user=user)
      send_mail_confirmation(user, get_current_site(self.request), slug, token, receiver=[user.email,])
      return reverse_lazy('auth:success', kwargs={'slug':slug})

# PAGE FOR CONFIRMATION LINK
def register_success_view(request, slug):
   user = get_object_or_404(Accounts, slug=slug)

   if request.method == 'GET':
      if user.is_active:
         return HttpResponseBadRequest()
   
   if request.method == 'POST':
      token = generate_token.make_token(user=user)
      send_mail_confirmation(user, get_current_site(request), slug, token, receiver=[user.email,])
   
   return render(request, template_name='auth/success.html')

# VALIDATION TOKEN
def validation_view(request, slug, token):
   if request.method == 'GET':

      user = get_object_or_404(Accounts, slug=slug)
      check_token = generate_token.check_token(user=user, token=token)
      if check_token and user.is_active==False:
         user.is_active = True
         user.save()
         return redirect(to=reverse_lazy('auth:login'))
      return HttpResponseBadRequest()
   
   return HttpResponseNotAllowed(permitted_methods=['post'])

# VIEW FOR LOGIN USER
class LoginUserView(FormView):
   http_method_names = ['get', 'post']
   template_name = 'auth/login.html'
   form_class = LoginForm
   success_url = reverse_lazy('home')

   def get_form_kwargs(self):
      kwargs = super().get_form_kwargs()
      kwargs['request'] = self.request
      return kwargs
   
   def form_valid(self, form):
      login(self.request, user=form.get_user)
      return super().form_valid(form)