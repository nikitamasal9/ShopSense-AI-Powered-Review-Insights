from django.db import models
from django.conf import settings

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
    
class ProductClick(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_clicks')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_clicks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='clicks')
    count = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return f"Buyer {self.buyer.username} clicked on {self.product.name} ({self.count} times)"

class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5) 
    emotion = models.CharField(max_length=50, default="neutral") 
    emotion_group = models.CharField(max_length=50, default="unknown") 
    intent = models.CharField(max_length=50)
    scope = models.CharField(max_length=50, default="general") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"