from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Accounts(AbstractUser):
   email = models.EmailField(verbose_name=_('email'), unique=True, blank=False)
   first_name = None
   last_name = None

   class Meta:
      db_table = 'accounts'
      verbose_name_plural = 'accounts'