from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=50)
    is_member = models.BooleanField(default=False)

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=4)


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

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='meal_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='favorites')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('customer', 'item')

    def __str__(self):
        return f"{self.customer.user.username} - {self.item.name}"


class Order(models.Model):
    order_number = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    prepared_at = models.DateTimeField(blank=True, null=True)
    cust_rating = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True,
        validators=[MaxValueValidator(5.0), MinValueValidator(0.0)]
    )
    delivery = models.BooleanField(default=True)
    items = models.ManyToManyField(Item, related_name='orders', through='OrderItem')

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.order.order_number}"


class ShoppingCart(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopping_cart')
    items = models.ManyToManyField(Item, related_name='carts')

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"


class Transaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(Customer, on_delete=models.CASCADE)
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for Order {self.order.order_number}"


class Analytics(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='monthly_analytics')
    month = models.DateField()  # Store the first day of the month
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True,
        validators=[MaxValueValidator(5.0), MinValueValidator(0.0)]
    )
    cust_views = models.IntegerField(default=0)
    avg_ticket = models.DecimalField(max_digits=8, decimal_places=2)
    total_sales = models.IntegerField(default=0)

    class Meta:
        unique_together = ('restaurant', 'month')

    def __str__(self):
        return f"Analytics for {self.restaurant.name} - {self.month.strftime('%B %Y')}"


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    items = models.ManyToManyField(Item, related_name='menus')

    def __str__(self):
        return self.name


class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_location = models.CharField(max_length=255)
    delivery_option = models.CharField(max_length=100)  # e.g., 'standard', 'priority'

    def str(self):
        return f"{self.user.username} - {self.delivery_option}"
