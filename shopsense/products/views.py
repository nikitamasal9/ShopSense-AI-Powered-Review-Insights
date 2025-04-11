from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django import forms
from .models import Product, ProductReview
from cart.models import Order, OrderItem
from django.urls import reverse
from django.db.models import Q

# def customer_reviews(request):
#     if request.method == 'POST':
#         review_text = request.POST.get('review')
#         if review_text:
#             # Send the review to the reviews app for analysis
#             response = requests.post('http://localhost:8000/reviews/api/analyze_review/', data={'review': review_text})
#             if response.status_code == 200:
#                 analysis_result = response.json()
#                 return JsonResponse(analysis_result)
#             else:
#                 return JsonResponse({'error': 'Failed to analyze review'}, status=500)
#     return render(request, 'products/customer_reviews.html')

# def subscribe(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         payment = request.POST.get('payment')
#         return HttpResponse("Subscription processed successfully!")
#     return render(request, 'products/subscribe.html')


# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('product_list')
#     else:
#         form = ProductForm()
#     return render(request, 'products/add_item.html', {'form': form})

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'products/product_list.html', {'products': products})

# @login_required
# def delete_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id, seller=request.user)
#     product.delete()  # Permanently delete the product from the database
#     messages.success(request, "Product deleted successfully.")
#     return redirect('products:seller_products')

@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('products:seller_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/update_item.html', {'form': form, 'product': product})

# def add_to_cart(request, product_id):
#     cart = request.session.get('cart', {})
#     cart[product_id] = cart.get(product_id, 0) + 1  
#     request.session['cart'] = cart 
#     return redirect('cart_view')

# def cart_view(request):
#     cart = request.session.get('cart', {})
#     products = Product.objects.filter(id__in=cart.keys())  
#     cart_items = [{'product': p, 'quantity': cart[str(p.id)]} for p in products]
#     return render(request, 'products/cart.html', {'cart_items': cart_items})

#At the top of your views.py file
from django.conf import settings
print("Template dirs:", settings.TEMPLATES[0]['DIRS'])

from transformers import pipeline
from rest_framework.response import Response
from rest_framework.views import APIView

# Load emotion and intent models
emotion_pipeline = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=1)
intent_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Emotion groups
EMOTION_GROUPS = {
    "happy": [
        "admiration", "amusement", "approval", "caring", "excitement",
        "gratitude", "joy", "love", "optimism", "pride", "relief", "surprise"
    ],
    "sadness": [
        "disappointment", "grief", "remorse", "sadness"
    ],
    "anger": [
        "anger", "annoyance", "disapproval", "disgust"
    ],
    "fear": [
        "embarrassment", "fear", "nervousness"
    ],
    "curiosity": [
        "confusion", "curiosity", "realization"
    ],
    "desire": [
        "desire"
    ],
    "neutral": [
        "neutral"
    ]
}

# Function to map an emotion to its group
def map_emotion_to_group(emotion_label):
    for group, labels in EMOTION_GROUPS.items():
        if emotion_label in labels:
            return group
    return "unknown"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(seller__username__icontains=query))
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)

    # Check if the user has purchased the product and the order is delivered
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='delivered'
        ).exists()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'has_purchased': has_purchased,
    })
@login_required
def add_product(request):
    if not request.user.is_seller():
        return HttpResponseForbidden("Only sellers can add products")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('products:seller_products')
    else:
        form = ProductForm()
    
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def seller_products(request):
    if not request.user.is_seller():
        return HttpResponseForbidden("Only sellers can view this page")
    
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/seller_products.html', {'products': products})


@login_required
def seller_orders(request):
    if not request.user.is_seller():
        return HttpResponseForbidden("Only sellers can view this page")
    
    # Get orders for products sold by the seller
    orders = Order.objects.filter(items__product__seller=request.user).distinct()
    
    return render(request, 'products/seller_orders.html', {'orders': orders})\
    

from django.shortcuts import redirect

@login_required
def update_order_status(request, order_id):
    if not request.user.is_seller():
        return HttpResponseForbidden("Only sellers can update order status")
    
    order = get_object_or_404(Order, id=order_id, items__product__seller=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {order.get_status_display()}")
        else:
            messages.error(request, "Invalid status")
    
    return redirect('products:seller_orders')

# filepath: c:\Users\dell\Desktop\test-project\django_ecommerce\products\views.py

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the user has purchased the product
    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
        order__status='delivered'
    ).exists()
    if not has_purchased:
        messages.error(request, "You can only review products you have purchased.")
        return redirect(reverse('products:product_detail', kwargs={'pk': product.id}))  # Use 'pk'

    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = int(request.POST.get('rating', 5))
        # emotion_result = emotion_pipeline(comment)
        # emotion = emotion_result[0][0]['label']

        # Emotion Classification
        emotion_result = emotion_pipeline(comment)
        specific_emotion = emotion_result[0][0]['label']
        emotion_group = map_emotion_to_group(specific_emotion)

        # Intent Classification
        intent_labels = ["praise intent", "complaint intent"]
        intent_result = intent_pipeline(comment, candidate_labels=intent_labels)
        intent = intent_result['labels'][0]  # Get the highest scoring label

        # Intent Classification (Specific Scope)
        intent_scope = [
            "packaging condition", 
            "delivery experience", 
            "overall product quality", 
            "value for money", 
            "product aesthetics", 
            "product durability"
        ]
        scope_result = intent_pipeline(comment, candidate_labels=intent_scope)
        scope = scope_result['labels'][0]

        # Save the review with emotion and intent
        ProductReview.objects.create(
            product=product,
            user=request.user,
            comment=comment,
            rating=rating,
            emotion=specific_emotion,  # Save emotion
            emotion_group=emotion_group,  # Save emotion group
            intent=intent,     # Save intent
            scope=scope  # Save scope
        )
        messages.success(request, "Your review has been added.")
        return redirect(reverse('products:product_detail', kwargs={'pk': product.id}))  # Use 'pk'

    return render(request, 'products/add_review.html', {'product': product})



@login_required
def subscribe(request):
    if not request.user.is_seller:
        messages.error(request, "Only sellers can subscribe.")
        return redirect('products:seller_products')

    # Hardcoded voucher for payment
    valid_voucher = "SUBSCRIBE123"

    if request.method == 'POST':
        entered_voucher = request.POST.get('voucher')
        if entered_voucher == valid_voucher:
            # Mark the user as subscribed
            request.user.subscribed = True
            request.user.save()
            messages.success(request, "Subscription successful! You can now access the dashboard.")
            return redirect('products:seller_products')
        else:
            messages.error(request, "Invalid voucher. Please try again.")

    return render(request, 'products/subscribe.html')
