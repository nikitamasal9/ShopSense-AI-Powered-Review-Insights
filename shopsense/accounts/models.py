from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    subscribed = models.BooleanField(default=False)  # Add this field for subscription

    def is_seller(self):
        return self.user_type == 'seller'

    def is_customer(self):
        return self.user_type == 'customer'