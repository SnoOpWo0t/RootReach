from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UpdateUserForm, ProfileUpdateForm

from products.models import Product,Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm
from django import forms
from products.models import Profile
from products.models import category # balpaknami
from django.shortcuts import render

def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('q', '')
        searched = Product.objects.filter(name__icontains=search_query)  # Adjust filters as needed
        return render(request, 'search.html', {
            'searched': searched,
            'search_query': search_query,
        })
    return render(request, 'search.html', {})




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

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,instance = current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'Your account has been updated.')
            return redirect('home')
        return render(request, 'update_profile.html', {'form': user_form})
    return render(request, 'update_profile.html', {})


def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html',{"categories":categories})



def product_page(request,pk):
    product = Product.objects.get(id= pk)
    return render(request, 'product.html',{'product':product})

def category(request,foo):
    foo = foo.replace('-', ' ') # it replaces hypen
    try :
        # category = Category.objects.get(name=foo)
        category = Category.objects.get(name__iexact=foo)

        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})
    except:
        messages.error(request, 'category does not exist')
        return redirect('home')

#update proile
@login_required
def update_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  # Ensure profile exists for user

    if request.method == 'POST':
        # Bind the forms with POST data, and instance for the user and profile
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        # Check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save user data
            profile_form.save()  # Save profile data
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('update_profile')  # Redirect to the same page to see the changes

    else:
        # If GET request, pass the instance of the user and profile to the forms
        user_form = UpdateUserForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    # Render the form in the template
    return render(request, 'update_profile.html', {'user_form': user_form, 'profile_form': profile_form})


#vew for seller
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from products.models import Product, Seller
from .forms import ProductForm  # Assume you have a ProductForm

# Seller homepage
@login_required
def seller_area(request):
    if not hasattr(request.user, 'seller'):  # Check if the user is a seller
        return redirect('home')  # If not, redirect to home page

    seller = request.user.seller
    products = Product.objects.filter(seller=seller)

    return render(request, 'seller_area.html', {'products': products})

# Product upload
@login_required
def upload_product(request, product_id=None):
    if not hasattr(request.user, 'seller'):
        return redirect('home')  # Only sellers can upload products

    # Editing product if product_id is provided
    if product_id:
        try:
            product = Product.objects.get(id=product_id, seller=request.user.seller)
        except Product.DoesNotExist:
            return redirect('home')  # Redirect if the product is not found
    else:
        product = None  # For new product upload

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # For editing, pass the product instance
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller  # Set the logged-in seller as the product seller
            product.save()  # Save the new or edited product
            return redirect('seller_area')  # Redirect to seller area after success
    else:
        form = ProductForm(instance=product)  # Prepopulate the form with the product for editing

    return render(request, 'upload_product.html', {'form': form, 'product': product})

# Delete product
@login_required

def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id, seller=request.user.seller)
        product.delete()
        return redirect('seller_area')
    except Product.DoesNotExist:
        return redirect('seller_area')  # or some other error page


#product edit
@login_required

def edit_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id, seller=request.user.seller)
    except Product.DoesNotExist:
        return redirect('seller_area')  # or some other page

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_area')  # Redirect to seller area after edit
    else:
        form = ProductForm(instance=product)

    return render(request, 'seller_area.html', {'form': form, 'product': product})
