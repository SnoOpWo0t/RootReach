from django.db import models
import datetime

from unicodedata import category

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/products/')
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

