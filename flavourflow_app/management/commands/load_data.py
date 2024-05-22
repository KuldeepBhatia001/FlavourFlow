from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from flavourflow_app.models import Customer, Restaurant, Item, Order, OrderItem, ShoppingCart, Transaction, Analytics, Menu, Favorite, Delivery
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Load sample data into the database'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Clear existing data
        Customer.objects.all().delete()
        Restaurant.objects.all().delete()
        Item.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        ShoppingCart.objects.all().delete()
        Transaction.objects.all().delete()
        Analytics.objects.all().delete()
        Menu.objects.all().delete()
        Favorite.objects.all().delete()
        Delivery.objects.all().delete()
        User.objects.all().exclude(is_superuser=True).delete()

        # Create Users and Customers
        for _ in range(5):
            user = User.objects.create_user(
                username=faker.user_name(),
                email=faker.email(),
                password='password123'
            )
            Customer.objects.create(
                user=user,
                phone=faker.phone_number(),
                payment_method=faker.credit_card_provider(),
                is_member=faker.boolean(),
                street=faker.street_address(),
                city=faker.city(),
                state=faker.state(),
                postcode=faker.postcode()
            )

        # Create Users and Restaurants
        for _ in range(10):
            user = User.objects.create_user(
                username=faker.user_name(),
                email=faker.email(),
                password='password123'
            )
            Restaurant.objects.create(
                user=user,
                name=faker.company(),
                phone=faker.phone_number(),
                abn=faker.ean(length=13),
                category=faker.word(),
                logo='restaurant_logo/sample_logo.jpg',
                street=faker.street_address(),
                city=faker.city(),
                state=faker.state(),
                postcode=faker.postcode()
            )

        customers = list(Customer.objects.all())
        restaurants = list(Restaurant.objects.all())

        # Create Items
        for _ in range(50):
            Item.objects.create(
                name=faker.word(),
                restaurant=random.choice(restaurants),
                price=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
                image='meal_images/sample_image.jpg',
                is_available=faker.boolean()
            )

        items = list(Item.objects.all())

        # Create Orders and OrderItems
        for _ in range(20):
            customer = random.choice(customers)
            restaurant = random.choice(restaurants)
            order = Order.objects.create(
                customer=customer.user,
                restaurant=restaurant,
                status=random.choice(['pending', 'completed', 'cancelled']),
                total_price=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
                cust_rating=random.uniform(0, 5),
                delivery=faker.boolean()
            )
            for _ in range(random.randint(1, 5)):
                OrderItem.objects.create(
                    order=order,
                    item=random.choice(items),
                    quantity=random.randint(1, 5)
                )

        # Create Shopping Carts
        for customer in customers:
            cart = ShoppingCart.objects.create(
                user=customer.user,
                total_price=faker.pydecimal(left_digits=2, right_digits=2, positive=True)
            )
            for _ in range(random.randint(1, 5)):
                cart.items.add(random.choice(items))

        # Create Transactions
        for order in Order.objects.all():
            Transaction.objects.create(
                order=order,
                amount=order.total_price,
                payment_method=order.customer.customer,
                payment_status=random.choice(['pending', 'success', 'failed'])
            )

        # Create Analytics
        for restaurant in restaurants:
            seen_months = set()
            for _ in range(12):  # 12 months
                month = faker.date_this_year(before_today=True, after_today=False)
                while month in seen_months:
                    month = faker.date_this_year(before_today=True, after_today=False)
                seen_months.add(month)
                Analytics.objects.create(
                    restaurant=restaurant,
                    month=month,
                    rating=random.uniform(0, 5),
                    cust_views=faker.random_int(min=0, max=500),
                    avg_ticket=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
                    total_sales=faker.random_int(min=0, max=500)
                )

        # Create Menus and add Items
        for restaurant in restaurants:
            menu = Menu.objects.create(
                restaurant=restaurant,
                name=faker.word(),
                description=faker.text(),
                is_active=faker.boolean()
            )
            for _ in range(random.randint(1, 10)):
                menu.items.add(random.choice(items))

        # Create Favorites
        for customer in customers:
            favorite_items = set()
            for _ in range(random.randint(1, 5)):
                item = random.choice(items)
                while (customer.id, item.id) in favorite_items:
                    item = random.choice(items)
                favorite_items.add((customer.id, item.id))
                Favorite.objects.create(
                    customer=customer,
                    item=item
                )

        # Create Deliveries
        for _ in range(20):
            Delivery.objects.create(
                user=random.choice(User.objects.all()),
                delivery_location=faker.address(),
                delivery_option=random.choice(['standard', 'priority'])
            )

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully'))
