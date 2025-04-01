from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login

from .forms import CustomerSignUpForm, SellerSignUpForm

# Create your views here.
def user_login(request):
  if request.method == 'POST':
    print(request.POST)
    return HttpResponse("Sign in page")
  return render(request, 'signin.html')

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            login(request, user)
            return HttpResponse("Customer dashboard")
            # return redirect('/customer/dashboard')
    else:
        form = CustomerSignUpForm()
    return render(request, 'customer_signup.html', {'form': form})

def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
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
    return render(request, 'onboarding.html')