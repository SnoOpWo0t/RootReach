from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': str(product.price)}
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def __len__(self):
        """ Return the total number of items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        """
        Mark the session as modified to ensure it is saved.
        """
        self.session.modified = True
    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()
        #use id to look up products in database
        products = Product.objects.filter(id__in=product_ids) #id te 2ta underscore lagbe ekta dile file error
<<<<<<< Updated upstream
        return products
=======
        return products

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()  # Ensure the cart is saved

>>>>>>> Stashed changes
