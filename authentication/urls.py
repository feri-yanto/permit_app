from django.urls import path
from .views import RegisterUserView

app_name = 'authentication'
urlpatterns = [
   path('register', view=RegisterUserView.as_view(), name='register'),
]