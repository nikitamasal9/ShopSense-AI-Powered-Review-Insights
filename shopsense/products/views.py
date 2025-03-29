from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.http import HttpResponse
from django.http import JsonResponse
import requests


def customer_reviews(request):
    if request.method == 'POST':
        review_text = request.POST.get('review')
        if review_text:
            # Send the review to the reviews app for analysis
            response = requests.post('http://localhost:8000/reviews/api/analyze_review/', data={'review': review_text})
            if response.status_code == 200:
                analysis_result = response.json()
                return JsonResponse(analysis_result)
            else:
                return JsonResponse({'error': 'Failed to analyze review'}, status=500)
    return render(request, 'products/customer_reviews.html')

def subscribe(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        payment = request.POST.get('payment')
        return HttpResponse("Subscription processed successfully!")
    return render(request, 'products/subscribe.html')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_item.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/confirm_delete.html', {'product': product})

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/update_item.html', {'form': form, 'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1  
    request.session['cart'] = cart 
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())  
    cart_items = [{'product': p, 'quantity': cart[str(p.id)]} for p in products]
    return render(request, 'products/cart.html', {'cart_items': cart_items})
