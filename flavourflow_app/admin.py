
from django.contrib import admin
from .models import Restaurant, Customer, Menu, MenuItem, Order, OrderItem, Transaction, Favourites, Analytics

admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Transaction)
admin.site.register(Favourites)
admin.site.register(Analytics)