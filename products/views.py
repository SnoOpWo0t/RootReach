from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from products.models import Product, Category

def category_summary(request, category_name):
    # Get the category object or return a 404 if it doesn't exist
    category = get_object_or_404(Category, name=category_name)
    # Filter products by the selected category
    products = Product.objects.filter(category=category)
    # Render the category page with the filtered products
    return render(request, 'category_summary.html', {})
