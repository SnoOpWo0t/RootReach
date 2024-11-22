from .cart import Cart

def cart_quantity(request):
    """
    Adds the total cart quantity to the context for all templates.
    """
    if request.user.is_authenticated:
        cart = Cart(request)
        return {'cart_quantity': len(cart)}
    return {'cart_quantity': 0}
