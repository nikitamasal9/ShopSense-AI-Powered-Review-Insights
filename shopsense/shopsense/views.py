# shopsense/views.py
from django.http import HttpResponse
from django.shortcuts import redirect, render

def home(request):
    return render(request, 'base.html')

def landing_page(request):
    if not request.user.is_authenticated:
        return redirect('/auth/signin')
    return render(request, 'landing.html')

