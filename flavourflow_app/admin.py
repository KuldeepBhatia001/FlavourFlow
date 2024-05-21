
from django.contrib import admin
from .models import Restaurant, Customer, Menu, Meal, Order, Transaction, Analytics, ItemList

admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(Analytics)