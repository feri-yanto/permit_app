from django.contrib.auth.tokens import PasswordResetTokenGenerator

class ConfirmTokenGenerator(PasswordResetTokenGenerator):
   def _make_hash_value(self, user, timestamp):
      return f"{user.pk}{user.is_active}{timestamp}"

generate_token = ConfirmTokenGenerator()