from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')

    phone = models.CharField(max_length=30, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, auto_now_add=True)
    intro = models.TextField()
    stuff_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Customer(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )

    name = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    category = models.CharField(max_length=30, choices=CATEGORY)
    description = models.TextField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='c_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='p_order')
    status = models.CharField(max_length=30, choices=STATUS)
    time_created = models.DateTimeField(auto_now_add=True)
