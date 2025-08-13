from django.contrib.auth.tokens import PasswordResetTokenGenerator

class ConfirmTokenGenerator(PasswordResetTokenGenerator):
   def _make_hash_value(self, user, timestamp):
      return f"{user.pk}{timestamp}"

generate_token = ConfirmTokenGenerator()