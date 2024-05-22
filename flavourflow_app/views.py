from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, authenticate;
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


def userSignin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request)
                messages.success(request, f'Welcome {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, "userSignin.html", {'form': form})


def userSignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request)
            messages.success(request, 'Registration successful')
            return redirect('userSignin')  # Redirect to home or another appropriate page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SignUpForm()

    return render(request, 'userSignup.html', {'form': form})


def login(request):
    return render(request, "registration/login.html")


@login_required
def user_dashboard(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    delivery_address = f"{customer.street}, {customer.city}, {customer.state}, {customer.postcode}" if customer.street else "No address specified"
    categories = Category.objects.all()
    food_items = Item.objects.all()
    favorites = Favorite.objects.filter(customer=customer)

    context = {
        'customer': customer,
        'delivery_address': delivery_address,
        'categories': categories,
        'food_items': food_items,
        'favorites': favorites
    }
    return render(request, 'user/dashboard.html', context)


def favorites(request):
    return render(render, 'user/favourites.html')

def shopping_cart(request):
    return render(render, 'user/shopping_cart.html')


def chat(request):
    return render(render, 'user/chat.html')


def history(request):
    return render(render, 'user/history.html')

def settings(request):
    return render(render, 'user/settings.html')


def restSignup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("restDashboard.html")
    else:
        form = UserCreationForm()
    return render(request, "registration/restSignup.html", {'form': form})


def restDashboard(request):
    return render(request, "restDashboard.html")


def flavourflow_app(request):
    return render(request, 'index.html')


# @login_required
def user_dashboard(request):
    return render(request, 'user/dashboard.html')



def favorites(request):
    return render(render, 'user/favorites.html')

def shopping_cart(request):
    return render(render, 'user/shopping_cart.html')


def chat(request):
    return render(render, 'user/chat.html')


def history(request):
    return render(render, 'user/history.html')

def settings(request):
    return render(render, 'user/settings.html')


# def membership(request):
#     pass
def membership(request):
    return render(request, 'membership.html')


@login_required
def home(request):
    return render(request, 'home.html')


def payments(request):
    if request.method == 'POST':
        return render(request, 'payments.html')

    return redirect('payments')


def checkoutOrder(request):
    delivery_option = request.session.get('delivery_option', 'standard')

    # Define delivery fees based on the options
    delivery_fees = {
        'priority': 3.99,
        'standard': 0.99,
        'schedule': 1.99,
    }

    try:
        # Get the user's shopping cart
        shopping_cart = request.user.shopping_cart
    except ObjectDoesNotExist:
        messages.error(request, 'You do not have a shopping cart. Please add items to your cart first.')
        return redirect('home')  # Redirect to the shopping cart page  setting to home to be changed later

    # Check if the shopping cart is empty
    if not shopping_cart.items.exists():
        messages.error(request, 'Your shopping cart is empty.')
        return redirect('home')  # Redirect to the shopping cart page setting to home to be changed later

    # Calculate the delivery fee
    delivery_fee = delivery_fees.get(delivery_option, 0.99)
    # Get the cart total
    cart_total = shopping_cart.total_price
    service_fee = 2.60
    total_price = cart_total + delivery_fee + service_fee

    return render(request, 'checkoutOrder.html', {
        'delivery_fee': delivery_fee,
        'total_price': total_price,
        'cart_total': cart_total
    })


def checkoutPayment(request):
    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST)
        payment_form = PaymentForm(request.POST)
        if delivery_form.is_valid() and payment_form.is_valid():
            # Save delivery information
            delivery = delivery_form.save(commit=False)
            delivery.user = request.user  # Assuming the user is logged in
            delivery.save()

            card_number = payment_form.cleaned_data['card_number']
            cvv = payment_form.cleaned_data['cvv']
            expiration_date = payment_form.cleaned_data['expiration_date']

            request.session['delivery_option'] = delivery.delivery_option

            # Redirect to the order tracking page
            return redirect('checkoutOrder')
    else:
        delivery_form = DeliveryForm()
        payment_form = PaymentForm()

    return render(request, 'checkoutPayment.html', {
        'delivery_form': delivery_form,
        'payment_form': payment_form
    })


def orderTracking(request):
    return render(request, 'orderTracking.html')

def settings(request):
    user = request.user
    context = {
        'username': user.username,
        'user_email': user.email,
    }
    return render(request, 'settings.html', context)
