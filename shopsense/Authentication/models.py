from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.
User = get_user_model()

class Customer(models.Model):
    role='customer'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Seller(models.Model):
    role = 'seller'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_title = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='sellers')  
    phone_number = models.CharField(max_length=15)
    business_address = models.TextField()
    subscription_status = models.BooleanField(default=False)
    subscription_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.business_title
