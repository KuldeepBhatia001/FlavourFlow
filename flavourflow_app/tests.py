from django.test import TestCase
from django.contrib.auth.models import User
from .models import Customer, Restaurant, Category, Item, Order, OrderItem, ShoppingCart, Transaction, Analytics, Menu, Delivery
from django.urls import reverse

class CustomerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Customer',
            phone='1234567890',
            street='Test Street',
            city='Test City',
            state='TS',
            postcode='1234'
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.user.username, 'testuser')
        self.assertEqual(str(self.customer), self.user.username)

class RestaurantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testrestaurant', password='password123')
        self.restaurant = Restaurant.objects.create(
            user=self.user,
            name='Test Restaurant',
            phone='0987654321',
            abn='12345678901',
            category='Fast Food',
            street='Restaurant Street',
            city='Restaurant City',
            state='RS',
            postcode='5678'
        )

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.user.username, 'testrestaurant')
        self.assertEqual(str(self.restaurant), self.restaurant.name)

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Test Category')

class ItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testrestaurant', password='password123')
        self.restaurant = Restaurant.objects.create(
            user=self.user,
            name='Test Restaurant',
            phone='0987654321',
            abn='12345678901',
            category='Fast Food',
            street='Restaurant Street',
            city='Restaurant City',
            state='RS',
            postcode='5678'
        )
        self.category = Category.objects.create(name='Test Category')
        self.item = Item.objects.create(
            name='Test Item',
            restaurant=self.restaurant,
            category=self.category,
            price=10.0
        )

    def test_item_creation(self):
        self.assertEqual(str(self.item), 'Test Item')

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Customer',
            phone='1234567890',
            street='Test Street',
            city='Test City',
            state='TS',
            postcode='1234'
        )
        self.restaurant_user = User.objects.create_user(username='testrestaurant', password='password123')
        self.restaurant = Restaurant.objects.create(
            user=self.restaurant_user,
            name='Test Restaurant',
            phone='0987654321',
            abn='12345678901',
            category='Fast Food',
            street='Restaurant Street',
            city='Restaurant City',
            state='RS',
            postcode='5678'
        )
        self.order = Order.objects.create(
            customer=self.user,
            restaurant=self.restaurant,
            total_price=20.0
        )

    def test_order_creation(self):
        self.assertEqual(str(self.order), f"Order {self.order.order_number}")

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    # def test_home_view(self):
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'home.html')

    def test_signup_view(self):
        response = self.client.get(reverse('userSignup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/userSignup.html')

    def test_login_view(self):
        response = self.client.get(reverse('userSignin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/userSignin.html')

    def test_logout_view(self):
        response = self.client.post(reverse('userLogout'))  # Use POST instead of GET
        self.assertEqual(response.status_code, 302)  # Redirect to login page
