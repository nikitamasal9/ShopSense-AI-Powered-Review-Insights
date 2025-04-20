from rest_framework import serializers
from .models import Product, ProductClick, ProductReview

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'

class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductClick
        fields = '__all__'