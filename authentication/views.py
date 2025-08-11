from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Accounts
from .forms import RegisterForm

# Create your views here.
class RegisterUserView(CreateView):
   http_method_names = ['get', 'post']
   template_name = 'auth/register.html'
   model = Accounts
   form_class = RegisterForm
   success_url = reverse_lazy('home')