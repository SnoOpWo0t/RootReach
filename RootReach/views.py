from django.shortcuts import render
from products.models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})
def about(request):

    return render(request, 'about.html',{})