from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from shopsense.models import Cart
from shopsense.models import Order, OrderItem

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

def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    cart_data = [{"name": item.product.name, "quantity": item.quantity} for item in cart_items]
    
    return JsonResponse({"cart_items": cart_data})


def add_to_cart(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')  
        product = next((p for p in demo_products if p['name'] == product_name), None)

        if product:
            cart = request.session.get('cart', {})
            cart[product_name] = cart.get(product_name, 0) + 1 
            request.session['cart'] = cart  
            request.session.modified = True  

            return redirect('cart_view')  

    return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_view(request):
    cart = request.session.get('cart', {})  # Get cart from session
    cart_items = [{'product': next((p for p in demo_products if p['name'] == name), None), 'quantity': qty} for name, qty in cart.items()]

    return render(request, 'cart.html', {'cart_items': cart_items})



def landing_page(request):
    if not request.user.is_authenticated:
        return redirect('/auth/signin')
    return render(request, 'landing.html')





@require_POST
def checkout(request):
    if request.user.is_authenticated:
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
 
        cart_items = cart.items.all()

        if not cart_items.exists():
            return JsonResponse({"success": False, "message": "Your cart is empty."})

        order = Order.objects.create(user=request.user)

       
        for item in cart_items:
            OrderItem.objects.create(order=order, product_name=item.product_name, quantity=item.quantity)

        cart_items.delete()


        return JsonResponse({"success": True, "message": "Order placed successfully!"})
    else:
        return JsonResponse({"success": False, "message": "You must be logged in to checkout."})

