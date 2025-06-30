from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=20, blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey('Client', on_delete=models.PROTECT, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    client = models.ForeignKey('Client', on_delete=models.PROTECT, related_name='orders')
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
