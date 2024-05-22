from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ("restaurant",)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class DeliveryForm(forms.ModelForm):
    DELIVERY_OPTIONS = [
        ('priority', 'Priority - 15-30 mins ($3.99)'),
        ('standard', 'Standard - 25-30 mins ($1.99)'),
        ('schedule', 'Schedule - Select a time')
    ]

    delivery_option = forms.ChoiceField(
        choices=DELIVERY_OPTIONS,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Delivery
        fields = ['delivery_location', 'delivery_option']
        widgets = {
            'delivery_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123 Street, Some Highway, Region, Country, Pin code'
            }),
        }


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Card Number'
        })
    )
    cvv = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CVV'
        })
    )
    expiration_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YY'
        })
    )

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
