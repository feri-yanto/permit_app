from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_mail_confirmation(receiver:list, context:dict):
   try:
      body = render_to_string(template_name='auth/confirm_email.html', context=context)
      email = EmailMultiAlternatives(
         subject='Verified your email',
         from_email=settings.EMAIL_HOST_USER,
         to=receiver,
      )
      email.attach_alternative(content=body, mimetype='text/html')
      email.send()
   except Exception as error:
      return False