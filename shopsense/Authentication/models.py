from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Customer(models.Model):
    role='customer'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.username

class Merchant(models.Model):
    role='merchant'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    business_address = models.TextField()

    def __str__(self):
        return self.business_name
    
