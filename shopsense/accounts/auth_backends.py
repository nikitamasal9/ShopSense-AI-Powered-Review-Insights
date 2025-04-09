# filepath: c:\Users\dell\Desktop\test-project\django_ecommerce\accounts\auth_backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerBackend(ModelBackend):
    """
    Custom authentication backend for customers.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_customer:
                return user
        except User.DoesNotExist:
            return None

class SellerBackend(ModelBackend):
    """
    Custom authentication backend for sellers.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_seller:
                return user
        except User.DoesNotExist:
            return None