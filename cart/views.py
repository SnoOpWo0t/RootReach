from itertools import product

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from products.models import Product


# Cart summary view
def cart_summary(request):
    """ Render the cart summary page."""
    cart = Cart(request)
    cart_products = cart.get_prods
    return render(request, "cart_summary.html", { "cart_products": cart_products})


# Add to cart view
@login_required
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)

        cart_quantity = len(cart)  # Total items in the cart
        response = JsonResponse({'qty': cart_quantity})
        return response



# Delete from cart view
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        return JsonResponse({'success': True, 'product_id': product_id})  # Return success
    return JsonResponse({'success': False, 'message': 'Invalid action!'})





# Update cart view
def cart_update(request):
    """
    Handle updating the quantity of a product in the cart.
    """
    if request.method == 'POST' and request.POST.get('action') == 'update':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        try:
            product_id = str(product_id)  # Ensure the ID is a string to match cart keys
            quantity = int(quantity)  # Ensure quantity is an integer
            cart.update(product_id, quantity)

            # Get the updated total quantity in the cart
            cart_quantity = len(cart.cart)

            # Return success response
            return JsonResponse({'qty': cart_quantity})
        except (ValueError, KeyError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)



# def cart_add(request):
#     """
#     Handle adding a product to the cart via AJAX POST request.
#     """
#     if request.method == 'POST' and request.POST.get('action') == 'post':
#         cart = Cart(request)
#         product_id = request.POST.get('product_id')
#
#         try:
#             product_id = int(product_id)  # Ensure product_id is an integer
#             product = get_object_or_404(Product, id=product_id)
#             cart.add(product)
#
#             # Get the total quantity in the cart
#             cart_quantity = len(cart.cart)
#
#             # Return success response
#             return JsonResponse({'qty': cart_quantity})
#         except (ValueError, Product.DoesNotExist):
#             return JsonResponse({'error': 'Invalid product ID'}, status=400)
#     return JsonResponse({'error': 'Invalid request'}, status=400)
