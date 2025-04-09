from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    # filepath: c:\Users\dell\Desktop\test-project\django_ecommerce\products\models.py
from django.conf import settings  # Import settings to reference AUTH_USER_MODEL

class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)  # Rating out of 5
    emotion = models.CharField(max_length=50, default="neutral")  # Add this field
    emotion_group = models.CharField(max_length=50, default="unknown")  # Add this field
    intent = models.CharField(max_length=50)
    scope = models.CharField(max_length=50, default="general")  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"