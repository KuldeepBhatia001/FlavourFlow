from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import *
from django.http import JsonResponse
from django.db.models import Count, F
from decimal import Decimal



def user_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            try:
                user.save()
                Customer.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    phone=form.cleaned_data['phone'],
                    payment_method=form.cleaned_data['payment_method'],
                    street=form.cleaned_data['street'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    postcode=form.cleaned_data['postcode'],
                )
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('userSignin')
            except IntegrityError:
                messages.error(request, 'A customer with this user already exists.')
                user.delete()  # Delete the user if the customer creation fails
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomerSignUpForm()
    return render(request, 'user/userSignup.html', {'form': form})


def user_signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/userSignin.html', {'form': form})



def user_signout(request):
    logout(request)
    return redirect('userSignin')


@login_required
def user_dashboard(request):
    try:
        customer = Customer.objects.get(user=request.user)
        delivery_address = f"{customer.street}, {customer.city}, {customer.state}, {customer.postcode}" if customer.street else "No address specified"
        categories = Category.objects.all()
        food_items = Item.objects.all()
        favorites = Favorite.objects.filter(customer=customer)
        restaurants = Restaurant.objects.all()

        context = {
            'customer': customer,
            'delivery_address': delivery_address,
            'categories': categories,
            'food_items': food_items,
            'favorites': favorites,
            'restaurants': restaurants
        }
        return render(request, 'user/dashboard.html', context)
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found. Please create a customer profile.")
        return redirect('userSignup')  # Redirect to a page where user can create a profile

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")
        return redirect('userSignup') 



"""
def userSignin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('dashboard/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, "user/userSignin.html", {'form': form})

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


# def login(request):
#     return render(request, "registration/login.html")


@login_required
def user_dashboard(request):
    customer=Customer.objects.get(user=request.user)
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

"""


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



@login_required
def favorites(request):
    customer = request.user.customer
    favorite_items = Favorite.objects.filter(customer=customer)

    context = {
        'favorite_items': favorite_items,
    }

    return render(request, 'user/favorites.html', context)

def shopping_cart(request):
    return render(request, 'user/shopping_cart.html')

def chat(request):
    return render(request, 'user/chat.html')

@login_required
def history(request):
    customer_orders = Order.objects.filter(customer=request.user)

    if request.method == "POST":
        item_id = request.POST.get('item_id')
        try:
            item = Item.objects.get(id=item_id)
            shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
            shopping_cart.items.add(item)
            shopping_cart.total_price += item.price
            shopping_cart.save()
            messages.success(request, f'Added {item.name} to your shopping cart.')
        except Item.DoesNotExist:
            messages.error(request, 'Item not found.')
        return redirect('order_history')

    context = {
        'customer_orders': customer_orders,
    }
    return render(request, 'user/history.html', context)

def settings(request):
    return render(request, 'user/settings.html')


def membership(request):
    return render(request, 'membership.html')

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    featured_items = Item.objects.filter(restaurant=restaurant, category__name='Featured')
    category_items = Item.objects.filter(restaurant=restaurant).exclude(category__name='Featured')

    context = {
        'restaurant': restaurant,
        'featured_items': featured_items,
        'category_items': category_items,
    }
    return render(request, 'user/restaurant_detail.html', context)

def restaurant_listing(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu = Menu.objects.filter(restaurant=restaurant, is_active=True).first()

    context = {
        'restaurant': restaurant,
        'menu': menu,
    }
    return render(request, 'user/restaurant_listing.html', context)

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    context = {
        'item': item,
    }
    return render(request, 'user/item_detail.html', context)

def items(request):
    items = Item.objects.all()
    return render(request, 'user/item_detail.html', {items})


"""
def restaurant_listing(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = Item.objects.filter(restaurant=restaurant)
    categories = Category.objects.all()
    categorized_items = {category: items.filter(category=category) for category in categories}
    featured_items = items[:3]  # Assuming the first 3 items are featured for simplicity

    context = {
        'restaurant': restaurant,
        'categorized_items': categorized_items,
        'featured_items': featured_items,
    }
    return render(request, 'user/restaurant_listing.html', context)
"""

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
        return redirect('dashboard')  # Redirect to the shopping cart page  setting to home to be changed later

    # Check if the shopping cart is empty
    if not shopping_cart.items.exists():
        messages.error(request, 'Your shopping cart is empty.')
        return redirect('dashboard')  # Redirect to the shopping cart page setting to home to be changed later

    # Calculate the delivery fee
    delivery_fee = delivery_fees.get(delivery_option, 0.99)
    # Get the cart total
    cart_total = shopping_cart.total_price
    service_fee = Decimal(str(2.60))
    total_price =  Decimal(str(cart_total)) +  Decimal(str((delivery_fee))) + service_fee

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

@login_required
def cart(request):
    try:
        # Retrieve the shopping cart for the logged-in user
        cart = ShoppingCart.objects.get(user=request.user)
        
        # Get the items from the shopping cart along with a count of each item
        cart_items = cart.items.annotate(quantity=Count('id')).order_by()

        # Calculate the total price
        total_price = sum(item.price * item.quantity for item in cart_items)

        cart.total_price = total_price  
        cart.save() # not able to load in db correctly

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        
        return render(request, 'user/shoppingcart.html', context)
    except ShoppingCart.DoesNotExist:
        return render(request, 'user/shoppingcart.html', {
            'cart_items': [], 
            'total_price': 0,
        })
    
@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        try:
            # Retrieve the shopping cart for the logged-in user
            cart = ShoppingCart.objects.get(user=request.user)

            # Retrieve the order item to be updated
            cart_items = OrderItem.objects.get(pk=item_id)

            # Update the quantity of the order item
            quantity = int(request.POST.get('quantity'))
            cart_items.quantity = quantity
            cart_items.save()

            # Calculate the total price
            total_price = sum(item.item.price * item.quantity for item in cart.items.all())

            # Return the updated total price as JSON response
            return JsonResponse({'total_price': total_price})
        except (ShoppingCart.DoesNotExist, OrderItem.DoesNotExist):
            return JsonResponse({'error': 'Could not update cart item.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            # Retrieve the shopping cart for the logged-in user
            cart = ShoppingCart.objects.get(user=request.user)

            # Retrieve the order item to be removed
            order_item = OrderItem.objects.get(pk=item_id)

            # Remove the order item from the cart
            cart.items.remove(order_item)

            # Calculate the total price
            total_price = sum(item.item.price * item.quantity for item in cart.items.all())

            # Return success response with the updated total price
            return JsonResponse({'total_price': total_price})
        except (ShoppingCart.DoesNotExist, OrderItem.DoesNotExist):
            return JsonResponse({'error': 'Could not remove item from cart.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

