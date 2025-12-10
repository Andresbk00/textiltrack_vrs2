from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) +
            six.text_type(timestamp) +
            six.text_type(user.email_verificado)
        )

email_verification_token = EmailVerificationTokenGenerator()

# Alias para compatibilidad con señales antiguas
token_verificacion = email_verification_token

