from django import forms
from django.contrib.auth.models import User
from .models import Customer, Seller

class CustomerSignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Customer
        fields = ['phone_number', 'address']

class SellerSignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Seller
        fields = ['business_title', 'phone_number', 'business_address']
