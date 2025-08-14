from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_mail_confirmation(accounts, domain, slug:str, token:str, receiver:list):
   try:
      send_mail(subject='Verified your email', message=render_to_string(
         template_name='auth/confirm_email.html',
         context={
            'name': accounts.username,
            'slug': slug,
            'token': token,
            'domain': domain,
         }
      ), from_email=settings.EMAIL_HOST_USER, recipient_list=receiver)
   except Exception as error:
      pass