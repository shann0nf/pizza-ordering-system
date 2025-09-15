from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta


class PizzaSize(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Cheese(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Sauce(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    SIZE_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large')
    ]

    CRUST_CHOICES = [
        ('Normal', 'Normal'),
        ('Thin', 'Thin'),
        ('Thick', 'Thick'),
        ('Gluten-Free', 'Gluten-Free')
    ]

    SAUCE_CHOICES = [
        ('Tomato', 'Tomato'),
        ('BBQ', 'BBQ')
    ]

    CHEESE_CHOICES = [
        ('Mozzarella', 'Mozzarella'),
        ('Vegan', 'Vegan'),
        ('Low Fat', 'Low Fat')
    ]

    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='Medium')
    crust = models.CharField(max_length=20, choices=CRUST_CHOICES, default='Normal')
    sauce = models.CharField(max_length=20, choices=SAUCE_CHOICES, default='Tomato')
    cheese = models.CharField(max_length=20, choices=CHEESE_CHOICES, default='Mozzarella')
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return f"{self.size} pizza with {self.crust} crust and {self.sauce} sauce"

    def get_formatted_pizza_description(self):
        """Format pizza description for display in the confirmation page."""
        toppings_list = ", ".join([topping.name for topping in self.toppings.all()])
        if not toppings_list:
            toppings_list = "No toppings"
        return f"{self.size} pizza with {self.crust} crust, {self.sauce} sauce, {self.cheese} cheese, and toppings: {toppings_list}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    payment_info = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    estimated_delivery_time = models.DateTimeField(default=now) 

    def save(self, *args, **kwargs):
        """ Automatically set estimated delivery time to 45 minutes after order_date """
        if not self.estimated_delivery_time:
            self.estimated_delivery_time = now() + timedelta(minutes=45)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - Delivery at {self.estimated_delivery_time}"
