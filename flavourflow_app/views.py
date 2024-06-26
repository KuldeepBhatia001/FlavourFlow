from decimal import Decimal

from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Count, Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from .forms import *
from .models import *



def flavourflow_app(request):
    return render(request, 'index.html')


# ==================================================================
# ========================= Restauraunt side =========================
# ==================================================================

def logout_view(request):
    logout(request)
    return redirect("rest_login")
def restSignup_view(request):
    if request.method == "POST":
        form = RestRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("restDashboard")
    else:
        form = RestRegisterForm()
    return render(request, "registration/restSignup.html", {'form': form})
@login_required(login_url='rest_login')
def restDashboard(request):
    user=request.user
    restaurant=Restaurant.objects.get(user=user)
    restaurant_name=restaurant.name
    user_name=user.get_full_name()
    return render(request, 'restDashboard.html',{'user_name':user_name,'restaurant_name':restaurant_name})

def restMenu(request):
        restaurant = Restaurant.objects.get(user=request.user)
        menus = Menu.objects.filter(restaurant=restaurant)
        selected_menu_name = request.GET.get('menu', '')
        selected_menu= None
        menu_items = {}
        for menu in menus:
            menu_items[menu.name] = menu.items.all()  # Fetch items for each menu

        if selected_menu_name:  # If a menu name is provided in the request
            selected_menu = get_object_or_404(Menu, name=selected_menu_name, restaurant=restaurant)

        return render(request, "restMenu.html", {"menus": menus, "menu_items": menu_items, "selected_menu": selected_menu})
@login_required(login_url='rest_login')
def get_menu_items(request):
    if request.method == 'GET' and request.is_ajax():
        menu_id = request.GET.get('menu_id')
        try:
            menu = Menu.objects.get(id=menu_id)
            items = menu.items.all()
            items_data = [{'name': item.name, 'description': item.description, 'price': item.price} for item in items]
            return JsonResponse({'items': items_data})
        except Menu.DoesNotExist:
            return JsonResponse({'error': 'Menu not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)
def edit_menu(request):
    restaurant = Restaurant.objects.get(user=request.user)
    items = Item.objects.filter(restaurant=restaurant)
    if request.method == 'POST':
        formset = MenuItemFormSet(request.POST, queryset=items)
        if formset.is_valid():
            formset.save()
            return redirect('restDashboard')  # Redirect to dashboard after saving
    else:
        formset = MenuItemFormSet(queryset=items)
        formset.restaurant = restaurant  # Pass the restaurant context to the formset
    return render(request, 'restMenu.html', {'formset': formset})

def restPerformance(request):
    # Calculate total revenue for the current month
    current_month_orders = Order.objects.filter(created_at__month=timezone.now().month)
    total_revenue = current_month_orders.aggregate(total_revenue=Sum('orderitem__item__price'))['total_revenue'] or 0

    # Calculate the number of orders for the current month
    total_orders = current_month_orders.count()

    return render(request, "restPerformance.html", {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
    })
def restOrders(request):
    user=request.user
    orders= Order.objects.prefetch_related('orderitem_set__item').all()
    return render(request,'restOrders.html',{'orders':orders})

@login_required(login_url='rest_login')
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(order_id)
        action = request.POST.get('action')  # Assuming you have a hidden input field in your form with name 'action'
        if action == 'accept':
            order.status = 'accepted'
            order.save()
            return HttpResponseRedirect(reverse('restOrders'))
        elif action == 'reject':
            order.status = 'rejected'
            order.save()
            return JsonResponse({'status': 'success', 'message': 'Order rejected'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required(login_url='rest_login')
def accept_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        order.status = 'accepted'
        order.save()
        return JsonResponse({'status': 'success','message':'Order accepted'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required(login_url='rest_login')
def reject_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        order.status = 'rejected'
        order.save()
        return JsonResponse({'status': 'success','message':'Order rejected'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

class RestLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({'placeholder': 'Email address'})
        form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        return render(request,'registration/login.html',{'form':form})
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=authenticate(request, username=email,password=password)
            if user is not None:
                login(request,user)
                try:
                    restaurant=Restaurant.objects.get(user=user)
                    return redirect("restDashboard")
                except Restaurant.DoesNotExist:
                    return render("registration/login.html", {'form':form})
            else:
                messages.error(request,'Invalid Credentials')
        return render(request,'registration/login.html',{'form':form,'error':'Invalid'})



# =============================================================
# ========================= User side =========================
# =============================================================

def signup_view(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('userSignin')  # Change 'home' to the name of your home page view
    else:
        form = CustomerSignupForm()
    return render(request, 'user/userSignup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/userSignin.html', {'form': form})


"""
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

"""

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
    food_items = Item.objects.all()
    return render(request, 'user/dashboard.html', {'food_items': food_items})




@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)

    if item not in cart.items.all():
        cart.items.add(item)
        cart.total_price += item.price
        cart.save()

    return redirect('dashboard')  # Redirect to the dashboard or wherever you want


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


# Cart views

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

# .Cart views