from django.urls import path
from . import views

from .views import *

urlpatterns = [
    path('', views.flavourflow_app, name='flavourflow_app'),

    path('signup/', views.user_signup, name='userSignup'),
    path('signin/', views.user_signin, name='userSignin'),

    path('signout/', views.user_signout, name='userSignout'),


    path('dashboard/', views.user_dashboard, name='user_dashboard'),


    # path('userSignin', views.userSignin, name='userSignin'),
    # path('userSignup', views.userSignup, name='userSignup'),
    path('restSignup/', views.restSignup_view, name='restSignup'),
    path('login/', views.login, name='login'),
    path('restDashboard/', views.restDashboard, name='restDashboard'),
    
    path('membership/', views.membership, name='membership'),
    path('payments/', views.payments, name='payments'),
    path('checkoutOrder/', views.checkoutOrder, name='checkoutOrder'),
    path('checkoutPayment/', views.checkoutPayment, name='checkoutPayment'),
    path('orderTracking/', views.orderTracking, name='orderTracking'),
    
    
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('favorites', views.favorites, name="favorites"),
    path('shopping_cart', views.shopping_cart, name="shopping_cart"),
    path('chat', views.chat, name="chat"),
    path('history', views.history, name="history"),
    path('settings', views.settings, name="settings"),


    path('items/',views.items, name="items"),
    
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/menu/<int:restaurant_id>/', views.restaurant_listing, name='restaurant_listing'),
    
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),


    path('cart/', views.cart, name='cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),




]
