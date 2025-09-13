from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.utils import timezone
from .models import PasswordResetToken

class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.email}{timestamp}"

password_reset_token_gen = CustomPasswordResetTokenGenerator()

def generate_reset_token(user):
    """Generate and store token, return (uid, token) for URL."""
    expires_at = timezone.now() + timezone.timedelta(hours=1)
    reset_token = PasswordResetToken.objects.create(user=user, expires_at=expires_at)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token_gen.make_token(user)  # Hashed for validation
    reset_token.token = token  # Store raw token for DB lookup
    reset_token.save()
    return uid, token

def validate_reset_token(uid, token):
    """Validate uid/token, return user and DB token obj or None."""
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid_decoded)
        db_token = PasswordResetToken.objects.get(user=user, token=token)
        if db_token.is_valid():
            return user, db_token
    except (ValueError, TypeError, User.DoesNotExist, PasswordResetToken.DoesNotExist):
        pass
    return None, None