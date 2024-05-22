from django.urls import path
from . import views

urlpatterns = [
    path('', views.flavourflow_app, name='flavourflow_app'),
    path('userSignin', views.userSignin, name='userSignin'),
    path('userSignup', views.userSignup, name='userSignup'),
    path('restSignup/', views.restSignup_view, name='restSignup'),
    path('login/', views.login, name='login'),
    path('restDashboard/', views.restDashboard, name='restDashboard'),
    
    path('membership/', views.membership, name='membership'),
    path('home/', views.home, name='home'),
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




]
