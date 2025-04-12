from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    subscribed = models.BooleanField(default=False) 
    subscription_start_date = models.DateTimeField(null=True, blank=True)  # Start date
    subscription_end_date = models.DateTimeField(null=True, blank=True)  # End date

    def is_seller(self):
        return self.user_type == 'seller'

    def is_customer(self):
        return self.user_type == 'customer'
    
    def has_active_subscription(self):
        return self.subscribed and self.subscription_end_date and self.subscription_end_date > now()