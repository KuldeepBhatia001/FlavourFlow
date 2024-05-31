from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import add_to_cart, RestLoginView, get_menu_items



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.flavourflow_app, name='flavourflow_app'),

    path('signup/', views.signup_view, name='userSignup'),
    path('login/', views.login_view, name='userSignin'),
    path('logout/', LogoutView.as_view(next_page='userSignin'), name='userLogout'),



    path('dashboard/', views.user_dashboard, name='user_dashboard'),


    # path('userSignin', views.userSignin, name='userSignin'),
    # path('userSignup', views.userSignup, name='userSignup'),
    path('restSignup/', views.restSignup_view, name='restSignup'),
    path('restlogin/', RestLoginView.as_view(), name='rest_login'),
    path('restDashboard/', views.restDashboard, name='restDashboard'),
    path('restdashboard/orders', views.restOrders, name='restOrders'),
    path('restdashboard/menu', views.restMenu, name='restMenu'),
    path('restdashboard/get_menu_items/', get_menu_items, name='get_menu_items'),
    path('edit_menu/', views.edit_menu, name='edit_menu'),
    path('restdashboard/performance', views.restPerformance, name='restPerformance'),

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

    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),

    
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/menu/<int:restaurant_id>/', views.restaurant_listing, name='restaurant_listing'),
    
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),


    path('cart/', views.cart, name='cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('logout/', views.logout_view, name='logout'),
    path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('reject_order/<int:order_id>/', views.reject_order, name='reject_order'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),


]
