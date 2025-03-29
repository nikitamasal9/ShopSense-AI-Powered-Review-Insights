# shopsense/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect

demo_products = [
    {'name': 'Laptop', 'price': 999, 'image': 'https://via.placeholder.com/150', 
     'description': 'A powerful laptop.', 'reviews': [
        {'reviewer': 'Alice', 'rating': 5, 'comment': 'Excellent laptop, very fast!'},
        {'reviewer': 'Bob', 'rating': 4, 'comment': 'Great performance, but a bit heavy.'}
     ]},
    {'name': 'Smartphone', 'price': 699, 'image': 'https://via.placeholder.com/150', 
     'description': 'A smartphone with a great camera.', 'reviews': [
        {'reviewer': 'Charlie', 'rating': 5, 'comment': 'Best phone I have ever owned!'}
     ]},
    {'name': 'Headphones', 'price': 199, 'image': 'https://via.placeholder.com/150', 
     'description': 'Noise-canceling headphones.', 'reviews': [
        {'reviewer': 'David', 'rating': 4, 'comment': 'Great sound quality, but a bit tight on my head.'}
     ]},
]

def home(request):
    return render(request, 'home.html', {'products': demo_products})

def product_detail(request, product_name):
    # Find the selected product
    selected_product = next((p for p in demo_products if p['name'] == product_name), None)

    if not selected_product:
        return render(request, '404.html', status=404)  # Handle missing product

    # Get related products (excluding the selected one)
    related_products = [p for p in demo_products if p['name'] != selected_product['name']]

    return render(request, 'product_detail.html', {'product': selected_product, 'related_products': related_products})


def product_detail(request, product_name):
    
    selected_product = next((p for p in demo_products if p['name'] == product_name), None)

    if not selected_product:
        return render(request, '404.html', status=404)  

    
    related_products = [p for p in demo_products if p['name'] != selected_product['name']]

    return render(request, 'product_detail.html', {'product': selected_product, 'related_products': related_products})


def landing_page(request):
    # if not request.user.is_authenticated:
    #     return redirect('/auth/signin')
    return render(request, 'landing.html')

def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')
def seller_dashboard(request):
    return render(request, 'seller_dashboard.html')