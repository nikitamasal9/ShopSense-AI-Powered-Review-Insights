from django import forms
from django.contrib.auth.models import User
from .models import Customer, Seller

class CustomerSignUpForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,  # Matches Django's User model max_length
        label="Username",
        help_text="Choose a unique username (max 150 characters)",
        required=True
    )
    email = forms.EmailField(
        label="Email Address",
        help_text="Enter a valid email address",
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        help_text="Enter a strong password",
        required=True
    )

    class Meta:
        model = Customer
        fields = ['phone_number', 'address']
        labels = {
            'phone_number': "Phone Number",
            'address': "Address",
        }
        help_texts = {
            'phone_number': "Enter your phone number",
            'address': "Enter your full address",
        }

    def save(self, commit=True):
        # Override save to handle User creation separately in the view
        customer = super().save(commit=False)
        if commit:
            customer.save()
        return customer

class SellerSignUpForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,  # Matches Django's User model max_length
        label="Username",
        help_text="Choose a unique username (max 150 characters)",
        required=True
    )
    email = forms.EmailField(
        label="Email Address",
        help_text="Enter a valid email address",
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        help_text="Enter a strong password",
        required=True
    )

    class Meta:
        model = Seller
        fields = ['business_title', 'phone_number', 'business_address']
        labels = {
            'business_title': "Business Title",
            'phone_number': "Phone Number",
            'business_address': "Business Address",
        }
        help_texts = {
            'business_title': "Enter your business name",
            'phone_number': "Enter your business phone number",
            'business_address': "Enter your business address",
        }

    def save(self, commit=True):
        # Override save to handle User creation separately in the view
        seller = super().save(commit=False)
        if commit:
            seller.save()
        return seller