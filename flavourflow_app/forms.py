from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *

class RestLoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ("restaurant",)

# class UserForm(forms.ModelForm):
#     email = forms.CharField(max_length=100, required=True)
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = Customer
#         fields = ("phone", "payment_method", "is_member", "street", "city", "state", "postcode")

# class UserFormForEdit(forms.ModelForm):
#     email = forms.CharField(max_length=100, required=True)

#     class Meta:
#         model = Customer
#         fields = ("user.first_name", "user.last_name")

# class RestaurantForm(forms.ModelForm):
#     class Meta:
#         model = Restaurant
#         fields = ("name", "phone", "address", "logo")

# class MenuForm(forms.ModelForm):
#     class Meta:
#         model = Menu
#         exclude = ("restaurant",)

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


# class PaymentForm(forms.Form):
#     # Payment fields as previously defined
#     card_number = forms.CharField(max_length=16)
#     expiration_date = forms.CharField(max_length=5)
#     cvv = forms.CharField(max_length=3)

# class DeliveryForm(forms.ModelForm):
#     class Meta:
#         model = Delivery
#         fields = ['delivery_location', 'delivery_option']
