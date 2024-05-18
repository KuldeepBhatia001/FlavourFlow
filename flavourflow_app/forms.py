from django import forms
from .models import User, Restaurant, Customer, Address, Menu, MenuItem,  Order, OrderItem, Payment

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