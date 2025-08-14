from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .views import RegisterUserView, LoginUserView, register_success_view, validation_view

app_name = 'authentication'
urlpatterns = [
   path('register', view=RegisterUserView.as_view(), name='register'),
   path('register/success/<str:slug>', view=register_success_view, name='success'),
   path('validation/<str:slug>/<str:token>', view=validation_view, name='validate'),
   path('login', view=LoginUserView.as_view(), name='login'),
   path('logout', view=login_required(function=LogoutView.as_view()), name='logout'),
]