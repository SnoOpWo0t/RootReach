from django.db import models
import datetime
from django.contrib.auth.models import User
from unicodedata import category
# from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'
#----------------------------Seller
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='seller_pics/', default='seller_pics/default.jpg')

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'

from django.db import models
from django.contrib.auth.models import User

#--------------------------
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/products/')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    #is_sale
    is_sale = models.BooleanField(default=False)
    sale_price = models.FloatField(default=0)
    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Order(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
   customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
   address = models.CharField(max_length=100)
   date = models.DateField(default=datetime.date.today)
   quantity = models.IntegerField(default=1)
   status = models.BooleanField(default=False)
   def __str__(self):
       return f'{self.product.name} {self.date} {self.quantity} {self.status}'



#profile information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    def __str__(self):
        return self.user.username
