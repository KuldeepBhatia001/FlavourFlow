rom django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from .models import *
from django.forms import modelformset_factory, ModelChoiceField
from .models import Item


class MenuItemFormSet(modelformset_factory(Item, fields=('name', 'price', 'image', 'is_available'), extra=0)):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Item.objects.none()

        # Add a field for selecting the menu
        menus = Menu.objects.filter(restaurant=self.restaurant)  # Assuming you have a ForeignKey from Menu to Restaurant
        self.fields['menu'] = ModelChoiceField(queryset=menus)
class RestLoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)

class RestRegisterForm(UserCreationForm):

    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(required=True)
    location=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    category=forms.CharField(max_length=100)
    phone=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model = User
        fields = ('email','password1','password2','name','location','category','phone')


class CustomerSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=500, required=True)
    phone = forms.CharField(max_length=10, required=True)
    payment_method = forms.CharField(max_length=50, required=True)
    street = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=255, required=True)
    state = forms.CharField(max_length=50, required=True)
    postcode = forms.CharField(max_length=4, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'phone', 'payment_method', 'street', 'city', 'state', 'postcode')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user



"""
class UserForm(forms.Form):
    username=forms.CharField(widget=forms.CharField)
    password=forms.CharField(widget=forms.PasswordInput)


"""
class MenuForm(forms.Form):
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
