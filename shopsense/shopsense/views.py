# shopsense/views.py
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'base.html')

def landing_page(request):
    return render(request, 'landing.html')


def sign_in(request):
    return HttpResponse("Sign in page")

def sign_up(request):
    return HttpResponse("Sign up page")