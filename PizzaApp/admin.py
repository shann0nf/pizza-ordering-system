from django.contrib import admin
from .models import PizzaSize, Cheese, Sauce, Topping, Pizza, Order


@admin.register(PizzaSize)
class PizzaSizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Cheese)
class CheeseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Sauce)
class SauceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'size', 'crust', 'sauce', 'cheese')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'estimated_delivery_time')
