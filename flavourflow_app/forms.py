from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Restaurant, Customer, Menu, MenuItem, Order, OrderItem, Payment, Delivery


class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ("username", "password", "first_name", "last_name", "email")


class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "email")


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("name", "phone", "address", "logo")


class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        exclude = ("restaurant",)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16)
    expiration_date = forms.CharField(label='Expiration Date', max_length=5)
    cvv = forms.CharField(label='CVV', max_length=3)


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['delivery_location', 'delivery_option']