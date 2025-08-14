from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

# Create your models here.
class Accounts(AbstractUser):
   slug = models.SlugField(verbose_name=_('slug'), unique=True, editable=False)
   email = models.EmailField(verbose_name=_('email'), unique=True, blank=False)
   first_name = None
   last_name = None

   class Meta:
      db_table = 'accounts'
      verbose_name_plural = 'accounts'
   
   def save(self, *args, **kwargs):
      if not self.slug and self.pk is None:  # Generate a slug only if it's not already set
         self.is_active = False
         self.slug = get_random_string(length=8)  # Generate an 8-character random string
         # Ensure uniqueness (optional, but recommended for slugs)
         while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug = get_random_string(length=8)
      super().save(*args, **kwargs)