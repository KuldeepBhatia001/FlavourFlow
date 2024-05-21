
from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(Item)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShoppingCart)
admin.site.register(Transaction)
admin.site.register(Analytics)