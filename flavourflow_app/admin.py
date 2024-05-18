
from django.contrib import admin
from .models import Restaurant, Customer, Address, Menu, MenuItem, Order, OrderItem, Payment

admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)