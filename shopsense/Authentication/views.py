from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def sign_in(request):
  if request.method == 'POST':
    print(request.POST)
    return HttpResponse("Sign in page")
  return render(request, 'signin.html')

def sign_up(request):
  if request.method == 'POST':
    print(request.POST)
    return HttpResponse("Sign up page")
  return render(request, 'signup.html')
