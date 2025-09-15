from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, PizzaForm, CheckoutForm
from .models import Order, Pizza
from django.contrib.auth.views import LoginView
from django.utils.timezone import now, localtime
from datetime import timedelta

# Index view
def index(request):
    return render(request, 'index.html')

# Register view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Orders view
@login_required
def orders(request):
    # Fetch all orders related to the logged-in user
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': user_orders})

# Create pizza view
@login_required
def create_pizza(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save()
            request.session['pizza_id'] = pizza.id
            return redirect('checkout') 
    else:
        form = PizzaForm()
    return render(request, 'create_pizza.html', {'form': form})

# Checkout view
@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            pizza = Pizza.objects.get(id=request.session['pizza_id'])

            
            placed_time = now()
            estimated_delivery_time = placed_time + timedelta(minutes=30)  

            # Create an order for the logged-in user
            Order.objects.create(
                user=request.user,
                pizza=pizza,
                delivery_address=form.cleaned_data['address'],
                payment_info=form.cleaned_data['card_number'],
                order_date=placed_time  
            )

            del request.session['pizza_id']  
            return redirect('confirmation')  
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form})

# Confirmation view
@login_required
def confirmation(request):
    order = Order.objects.filter(user=request.user).last()
    
    if order:
        placed_time = localtime(order.order_date)  
        estimated_delivery_time = placed_time + timedelta(minutes=30) 
        return render(request, 'confirmation.html', {
            'order': order,
            'formatted_pizza': order.pizza.get_formatted_pizza_description(),  
            'placed_time': placed_time,
            'estimated_delivery_time': estimated_delivery_time
        })

    return render(request, 'confirmation.html', {'order': None}) 

class CustomLoginView(LoginView):
    def get_success_url(self):
        return '/orders/'
