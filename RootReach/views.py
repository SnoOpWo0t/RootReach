from django.shortcuts import render, redirect
from products.models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})
def about(request):
    return render(request, 'about.html',{})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
             messages.success(request, 'there was an error')
        return redirect('login')
    else:

        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')
