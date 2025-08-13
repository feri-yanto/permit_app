from django.views.generic import CreateView, FormView
from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.messages import get_messages, success
from django.conf import settings
from django.contrib.auth import login
from .models import Accounts
from .forms import RegisterForm, LoginForm
from .tokens import generate_token

# VIEW FOR REGISTER NEW USER
class RegisterUserView(CreateView):
   http_method_names = ['get', 'post']
   template_name = 'auth/register.html'
   model = Accounts
   form_class = RegisterForm

   def get_success_url(self):
      created_user = self.object
      uid = urlsafe_base64_encode(force_bytes(created_user.id))
      token = generate_token.make_token(user=created_user)
      send_mail(subject='Verified your email', message=render_to_string(
         template_name='auth/confirm_email.html',
         context={
            'name': created_user.username,
            'id': uid,
            'token': token,
            'domain': get_current_site(self.request)
         }
      ), from_email=settings.EMAIL_HOST_USER, recipient_list=['feriiiyanto.i7@gmail.com',])
      success(self.request, message='berhasil')
      return reverse_lazy('auth:success')

# VIEW FOR SUCCESS REGISTER ONLY
def register_success_view(request):
   if request.method == 'GET':

      storage = get_messages(request)
      if storage.__len__() > 0:
         return render(request, template_name='auth/success.html')
      
      return HttpResponseBadRequest()
   return HttpResponseNotAllowed(permitted_methods=['get'])

# VIEW FOR CONFIRMATION EMAIL
def confirm_user(request, id, token):
   if request.method == 'GET':
      uid = force_str(urlsafe_base64_decode(id))
      user = get_object_or_404(Accounts, id=int(uid))
      
      is_token_valid = generate_token.check_token(user, token=token)
      if is_token_valid:
         user.is_active = True
         user.save()
         return redirect(to='/auth/login')

      return HttpResponseBadRequest()
   return HttpResponseNotAllowed(permitted_methods='get')

# VIEW FOR USER LOGIN
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