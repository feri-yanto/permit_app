from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .views import RegisterUserView, LoginUserView, register_success_view, confirm_user

app_name = 'authentication'
urlpatterns = [
   path('register', view=RegisterUserView.as_view(), name='register'),
   path('register/success', view=register_success_view, name='success'),
   path('login', view=LoginUserView.as_view(), name='login'),
   path('logout', view=login_required(function=LogoutView.as_view(), login_url='/auth/login'), name='logout'),
   path('validation/<str:id>/<str:token>', view=confirm_user, name='validation')
]