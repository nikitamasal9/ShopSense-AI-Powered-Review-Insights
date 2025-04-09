# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Sum, F, DecimalField
from django.db import transaction
from decimal import Decimal
from products.models import Product
from .models import CartItem, Order, OrderItem
from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

@login_required
def view_cart(request):
    if request.user.is_seller():
        return HttpResponseForbidden("Sellers cannot have a shopping cart")
    
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.get_total_price() for item in cart_items)
    
    return render(request, 'cart/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def add_to_cart(request, product_id):
    if request.user.is_seller():
        return HttpResponseForbidden("Sellers cannot have a shopping cart")
    
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart")
    return redirect('products:product_detail', pk=product_id)

@login_required
def update_cart_item(request, item_id):
    if request.user.is_seller():
        return HttpResponseForbidden("Sellers cannot have a shopping cart")
    
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
    
    return redirect('cart:view_cart')

@login_required
def remove_from_cart(request, item_id):
    if request.user.is_seller():
        return HttpResponseForbidden("Sellers cannot have a shopping cart")
    
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f"{product_name} removed from your cart")
    return redirect('cart:view_cart')

@login_required
def checkout(request):
    if request.user.is_seller():
        return HttpResponseForbidden("Sellers cannot have a shopping cart")
    
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect('products:product_list')
    
    total_price = sum(item.get_total_price() for item in cart_items)
    form = CheckoutForm(initial={'email': request.user.email})
    
    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })

@login_required
@transaction.atomic
def place_order(request):
    if request.user.is_seller():
        return HttpResponseForbidden("Sellers cannot have a shopping cart")
    
    if request.method != 'POST':
        return redirect('cart:checkout')
    
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect('products:product_list')
    
    form = CheckoutForm(request.POST)
    
    if form.is_valid():
        total_price = sum(item.get_total_price() for item in cart_items)
        
        # Create the order
        order = Order.objects.create(
            user=request.user,
            full_name=form.cleaned_data['full_name'],
            email=form.cleaned_data['email'],
            address=form.cleaned_data['address'],
            city=form.cleaned_data['city'],
            state=form.cleaned_data['state'],
            zip_code=form.cleaned_data['zip_code'],
            total_price=total_price
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )
        
        # Empty the cart
        cart_items.delete()
        
        return redirect('cart:order_confirmation', order_id=order.id)
    
    # If form is invalid, return to checkout
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_confirmation.html', {'order': order})

@login_required
def my_orders(request):
    if request.user.is_seller():
        return HttpResponseForbidden("Sellers cannot place orders")
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cart/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_detail.html', {'order': order})

