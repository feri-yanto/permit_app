from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .views import RegisterUserView
from .forms import LoginForm

app_name = 'authentication'
urlpatterns = [
   path('register', view=RegisterUserView.as_view(), name='register'),
   path('login', view=LoginView.as_view(
      template_name='auth/login.html',
      form_class=LoginForm,
   ), name='login'),
   path('logout', view=login_required(function=LogoutView.as_view()), name='logout'),
]