from django.db import models
from django.contrib.auth.models import User
import json


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=50)
    is_member = models.BooleanField(default=False)

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=4)

    favourites = models.JSONField(default=list)

    def add_fav(self, restaurant_id):
        if restaurant_id not in self.favourites:
            self.favourites.append(restaurant_id)
        self.save()

    def remove_fav(self, restaurant_id):
        if restaurant_id in self.favourites:
            self.favourites.remove(restaurant_id)
            self.save()

    def get_fav(self):
        return self.favourites  # returns array I think


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')

    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=10)
    abn = models.CharField(max_length=11, unique=True)
    category = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='restaurant_logo/')

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=4)


class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='meal_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

# -------------------------------------------------------------------------------


class ItemList(models.Model):
    items = models.JSONField(default=dict)

    def add_item(self, item_id, quantity):
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity
        self.save()

    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
            self.save()

    def get_items(self):
        return list(self.items.items())


class Menu(ItemList):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)


class Order(ItemList):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    status = models.CharField(max_length=10, default='pending')
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    prepared_at = models.DateTimeField(blank=True, null=True)
    cust_rating = models.DecimalField(max_digits=5, decimal_places=1)
    delivery = models.BooleanField(default=True)


class ShoppingCart(ItemList):
    total_price = models.DecimalField(max_digits=5, decimal_places=2)

# ------------------------------------------------------------------------------


class Transaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_method = models.ForeignKey(Customer, on_delete=models.CASCADE)
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)


class Analytics(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='monthly_analytics')
    month = models.DateField()  # Store the first day of the month
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    cust_views = models.IntegerField(default=0)
    avg_ticket = models.DecimalField(max_digits=8, decimal_places=2)
    total_sales = models.IntegerField(default=0)

    class Meta:
        unique_together = ('restaurant', 'month')
