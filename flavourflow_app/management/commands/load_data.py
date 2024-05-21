import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from flavourflow_app.models import *
from django.utils import timezone
from faker import Faker

class Command(BaseCommand):
    help = 'Load sample data into the database'

    def handle(self, *args, **kwargs):
        # Clear the database
        Customer.objects.all().delete()
        Restaurant.objects.all().delete()
        Menu.objects.all().delete()
        MenuItem.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        Transaction.objects.all().delete()
        Analytics.objects.all().delete()
        Favourites.objects.all().delete()
        User.objects.all().delete()

        fake = Faker()

        # Create sample users
        user1 = User.objects.create_user(username='customer1', password='password1', email=fake.email())
        user2 = User.objects.create_user(username='customer2', password='password2', email=fake.email())
        user3 = User.objects.create_user(username='restaurant1', password='password3', email=fake.email())

        # Create sample customers
        customer1 = Customer.objects.create(
            user=user1,
            payment_method=fake.credit_card_provider(),
            is_member=True,
            phone=fake.phone_number()[:10],
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            postcode=fake.zipcode()[:4]
        )

        customer2 = Customer.objects.create(
            user=user2,
            payment_method=fake.credit_card_provider(),
            is_member=False,
            phone=fake.phone_number()[:10],
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            postcode=fake.zipcode()[:4]
        )

        # Create sample restaurant
        restaurant = Restaurant.objects.create(
            user=user3,
            name=fake.company(),
            phone=fake.phone_number()[:10],
            abn=fake.bban()[:11],
            category=fake.word(),
            logo='static/media/recipe_1.png',
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            postcode=fake.zipcode()[:4]
        )

        # Create sample menus
        menu = Menu.objects.create(
            restaurant=restaurant,
            name='Lunch Menu',
            description='Delicious lunch items',
            is_active=True
        )

        # Create sample menu items
        menu_item1 = MenuItem.objects.create(
            menu=menu,
            restaurant=restaurant,
            name='Spaghetti',
            description='Classic Italian pasta dish',
            price=12.99,
            image='static/media/menu_item_images/spaghetti.png',
            is_available=True
        )

        menu_item2 = MenuItem.objects.create(
            menu=menu,
            restaurant=restaurant,
            name='Lasagna',
            description='Hearty lasagna with meat and cheese',
            price=15.99,
            image='static/media/menu_item_images/lasagna.png',
            is_available=True
        )

        # Create sample orders
        order1 = Order.objects.create(
            customer=user1,
            restaurant=restaurant,
            status='pending',
            total_price=28.98,
            created_at=timezone.now(),
            prepared_at=None,
            cust_rating=4.5,
            delivery=True
        )

        order2 = Order.objects.create(
            customer=user2,
            restaurant=restaurant,
            status='completed',
            total_price=15.99,
            created_at=timezone.now(),
            prepared_at=timezone.now(),
            cust_rating=5.0,
            delivery=False
        )

        # Create sample order items
        OrderItem.objects.create(
            order=order1,
            menu_item=menu_item1,
            quantity=2,
            price=25.98,
            notes='Extra cheese'
        )

        OrderItem.objects.create(
            order=order2,
            menu_item=menu_item2,
            quantity=1,
            price=15.99,
            notes='No onions'
        )

        # Create sample transactions
        Transaction.objects.create(
            order=order1,
            amount=28.98,
            payment_method=customer1,
            payment_status='success',
            timestamp=timezone.now()
        )

        Transaction.objects.create(
            order=order2,
            amount=15.99,
            payment_method=customer2,
            payment_status='success',
            timestamp=timezone.now()
        )

        # Create sample analytics
        Analytics.objects.create(
            restaurant=restaurant,
            month=timezone.now().replace(day=1),
            rating=4.5,
            cust_views=100,
            avg_ticket=20.00,
            total_sales=1500
        )

        # Create sample favourites
        Favourites.objects.create(
            customer=customer1,
            order=restaurant
        )

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully'))
