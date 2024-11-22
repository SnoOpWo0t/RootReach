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
        """
        Return the total number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        """
        Mark the session as modified to ensure it is saved.
        """
        self.session.modified = True
