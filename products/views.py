from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from products.models import Product, Category
def categories(request):
    return {'categories': Category.objects.all()}
def category_summary(request, category_name):

    category = get_object_or_404(Category, name=category_name)

    products = Product.objects.filter(category=category)

    return render(request, 'category_summary.html', {})
