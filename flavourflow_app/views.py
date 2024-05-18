from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

def userSignin(request):
    return render(request, "userSignin.html")


def userSignup(request):
    return render(request, "userSignup.html")


def flavourflow_app(request):
    return render(request, 'index.html')


# Sanjit - need to implement login encapsulation
def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'home.html', {'restaurants': restaurants}) # change template name as required

def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menus = Menu.objects.filter(restaurant=restaurant, is_active=True)
    return render(request, 'restaurant_menu.html', {'restaurant': restaurant, 'menus': menus}) # change template name

# for menu editing
def menu_view(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    menu_items = MenuItem.objects.filter(menu=menu, is_available=True)
    return render(request, 'menu_view.html', {'menu': menu, 'menu_items': menu_items}) # change template name

def order_track(request):
    return render(request, 'order_track.html')