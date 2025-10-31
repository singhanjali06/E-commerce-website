from django.contrib import admin
from .models import CustomUser, Vendor, Product, Order, OrderItem
from .models import CartItem


# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)

