from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# klasy odpowiedzialne za generowanie tokenów bezpieczeństa
# w tym przypadku do przesyłania linku restarującego hasło

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp)  + text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()