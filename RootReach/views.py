from django.shortcuts import render
from products.models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})