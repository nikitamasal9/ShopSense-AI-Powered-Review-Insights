from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages


from .forms import CustomerSignUpForm, SellerSignUpForm

# Create your views here.
def user_login(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = User.objects.get(email=email)
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('/')
        else:
            messages.error(request, "Invalid email or password.")
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
  return render(request, 'signin.html')
  
def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'],password=form.cleaned_data['password'])
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            login(request, user)
            return render("/")
            # return redirect('/customer/dashboard')
    else:
        form = CustomerSignUpForm()
    return render(request, 'customer_signup.html', {'form': form})

def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            seller = form.save(commit=False)
            seller.user = user
            seller.save()
            login(request, user)
            return HttpResponse("Seller dashboard")
            # return redirect('/seller/dashboard')
    else:
        form = SellerSignUpForm()
    return render(request, 'seller_signup.html', {'form': form})


def onboarding(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'customer':
            return redirect('customer_signup')
        elif user_type == 'seller':
            return redirect('seller_signup')
        messages.error(request, "Please select a valid user type.")
    return render(request, 'onboarding.html')

def user_logout(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect('home')
    return render(request, 'logout.html')