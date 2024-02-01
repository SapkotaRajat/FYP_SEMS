# user_authentication/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, email_or_username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=email_or_username)  # Assuming email_or_username is unique
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
