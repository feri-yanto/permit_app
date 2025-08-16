from django.views.generic import CreateView, FormView
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_http_methods, require_GET
from django.urls import reverse_lazy
from .models import Accounts
from .forms import RegisterForm
from .tokens import generate_token
from .mail import send_mail_confirmation

# VIEW FOR REGISTER NEW USER
class RegisterUserView(CreateView):
   http_method_names = ['get', 'post']
   template_name = 'auth/register.html'
   model = Accounts
   form_class = RegisterForm
   
   def form_valid(self, form):
      response = super().form_valid(form)
      new_user = self.object
      user_token = generate_token.make_token(user=new_user)
      # Send email to user
      send_mail_confirmation(receiver=[new_user.email,], context={
         'name': new_user.username,
         'slug': new_user.slug,
         'token': user_token,
         'domain': get_current_site(request=self.request).domain,
      })
      return response
   
   def get_success_url(self):
      return reverse_lazy('auth:success', kwargs={'slug':self.object.slug})

# PAGE FOR CONFIRMATION LINK
@require_http_methods(request_method_list=['GET', 'POST'])
def register_success_view(request, slug):
   user = get_object_or_404(Accounts, slug=slug)

   if request.method == 'GET':
      if user.is_active:
         return redirect(to=reverse_lazy('auth:login'))
   
   if request.method == 'POST':
      new_token = generate_token.make_token(user=user)
      send_mail_confirmation(receiver=[user.email,], context={
         'name': user.username,
         'slug': user.slug,
         'token': new_token,
         'domain': get_current_site(request=request).domain,
      })
   
   return render(request, template_name='auth/success.html')

# VALIDATION TOKEN
@require_GET
def validation_view(request, slug, token):
   user = get_object_or_404(Accounts, slug=slug)
   check_token = generate_token.check_token(user=user, token=token)
   if check_token and not user.is_active:
      user.is_active = True
      user.save()
      return redirect(to=reverse_lazy('auth:login'))
   return HttpResponseBadRequest('Link sudah tidak valid')