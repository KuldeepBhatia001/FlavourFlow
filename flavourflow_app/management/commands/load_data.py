import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from flavourflow_app.models import *


# Sample arrays for generating random data
first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana"]
last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones"]
streets = ["Main St", "High St", "Park Ave", "Broadway", "Sunset Blvd", "Maple St"]
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"]
states = ["NY", "CA", "IL", "TX", "AZ", "PA"]
categories = ["Fast Food", "Italian", "Chinese", "Mexican", "Indian", "Japanese"]
restaurant_names = ["The Great Eatery", "Food Paradise", "Taste of Heaven", "Gourmet Delight", "Food Fiesta", "Culinary Haven"]
item_names = ["Burger", "Pizza", "Sushi", "Tacos", "Pasta", "Salad"]
delivery_options = ["standard", "priority"]

def random_phone():
    return ''.join(random.choices('0123456789', k=10))

def random_postcode():
    return ''.join(random.choices('0123456789', k=4))

def random_abn():
    return ''.join(random.choices('0123456789', k=11))

def generate_unique_username(base):
    username = base
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1
    return username

class Command(BaseCommand):
    help = 'Populate the database with random data'

    def handle(self, *args, **kwargs):

        # Clear existing data
        Delivery.objects.all().delete()
        Menu.objects.all().delete()
        Analytics.objects.all().delete()
        Transaction.objects.all().delete()
        ShoppingCart.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Item.objects.all().delete()
        Category.objects.all().delete()
        Restaurant.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create users
        for _ in range(10):
            base_username = f'user{random.randint(1, 1000)}'
            username = generate_unique_username(base_username)
            email = f'{username}@example.com'
            password = 'password123'
            user = User.objects.create_user(username=username, email=email, password=password)
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Create customer
            Customer.objects.create(
                user=user,
                name=f'{first_name} {last_name}',
                phone=random_phone(),
                street=random.choice(streets),
                city=random.choice(cities),
                state=random.choice(states),
                postcode=random_postcode()
            )

        # Create categories
        for category in categories:
            Category.objects.create(name=category)

        # Create restaurants
        for _ in range(20):
            base_username = f'restaurant{random.randint(1, 1000)}'
            username = generate_unique_username(base_username)
            email = f'{username}@example.com'
            password = 'password123'
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            Restaurant.objects.create(
                user=user,
                name=random.choice(restaurant_names),
                phone=random_phone(),
                abn=random_abn(),
                category=random.choice(categories),
                street=random.choice(streets),
                city=random.choice(cities),
                state=random.choice(states),
                postcode=random_postcode()
            )

        # Create items
        restaurants = Restaurant.objects.all()
        for restaurant in restaurants:
            for _ in range(10):
                item_name = random.choice(item_names)
                category = random.choice(Category.objects.all())
                Item.objects.create(
                    name=item_name,
                    restaurant=restaurant,
                    category=category,
                    price=round(random.uniform(5.0, 50.0), 2)
                )

        # Create orders
        customers = Customer.objects.all()
        for customer in customers:
            restaurant = random.choice(restaurants)
            order = Order.objects.create(
                customer=customer.user,
                restaurant=restaurant,
                total_price=round(random.uniform(20.0, 100.0), 2),
                delivery=random.choice([True, False])
            )
            items = random.sample(list(Item.objects.filter(restaurant=restaurant)), k=3)
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    item=item,
                    quantity=random.randint(1, 5)
                )

        # Create shopping carts
        for customer in customers:
            if not ShoppingCart.objects.filter(user=customer.user).exists():
                shopping_cart = ShoppingCart.objects.create(
                    user=customer.user,
                    total_price=round(random.uniform(20.0, 100.0), 2)
                )
                items = random.sample(list(Item.objects.all()), k=5)
                shopping_cart.items.set(items)
                shopping_cart.save()

        # Create transactions
        for order in Order.objects.all():
            if not Transaction.objects.filter(order=order).exists():
                Transaction.objects.create(
                    order=order,
                    amount=order.total_price,
                    payment_status=random.choice(['pending', 'success', 'failed'])
                )

        # Create analytics
        for restaurant in restaurants:
            for _ in range(12):  # One entry per month for the last year
                month = random.choice(range(1, 13))
                year = random.choice(range(2021, 2023))
                date = f'{year}-{month:02d}-01'
                if not Analytics.objects.filter(restaurant=restaurant, month=date).exists():
                    Analytics.objects.create(
                        restaurant=restaurant,
                        month=date,
                        rating=round(random.uniform(0.0, 5.0), 2),
                        cust_views=random.randint(0, 500),
                        avg_ticket=round(random.uniform(10.0, 50.0), 2),
                        total_sales=random.randint(0, 1000)
                    )

        # Create menus
        for restaurant in restaurants:
            for _ in range(3):
                menu = Menu.objects.create(
                    restaurant=restaurant,
                    name=f"Menu {_+1}",
                    description="A delicious selection of items",
                    is_active=random.choice([True, False])
                )
                items = random.sample(list(Item.objects.filter(restaurant=restaurant)), k=5)
                menu.items.set(items)
                menu.save()

        # Create deliveries
        for customer in customers:
            for _ in range(3):
                Delivery.objects.create(
                    user=customer.user,
                    delivery_location=random.choice(streets),
                    delivery_option=random.choice(delivery_options)
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with random data'))
