from django.shortcuts import render, redirect
from unicodedata import category

from products.models import Product,Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

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
#register
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')  # Use password1 for raw password
            # Authenticate the user
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been registered successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed. Please try logging in.')
        else:
            # Add form errors to messages for better debugging
            error_messages = form.errors.as_data()  # Extract raw errors
            for field, errors in error_messages.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})
# def register_user(request):
#     form = SignUpForm()
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             #log in user
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, 'You have been registered')
#             return redirect('home')
#         else:
#             messages.success(request, 'not registered')
#             return redirect('register')
#
#     else:
#         return render(request, 'register.html',{'form':form})
def product_page(request,pk):
    product = Product.objects.get(id= pk)
    return render(request, 'product.html',{'product':product})

def category_page(request,foo):
    foo = foo.replace('_', ' ') # it replaces hypen
    try :
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})
    except:
        messages.error(request, 'category does not exist')
        return redirect('home')


