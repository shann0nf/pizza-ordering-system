from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', CustomLoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('orders/', views.orders, name="orders"),
    path('order/new/', views.create_pizza, name="create_pizza"),
    path('checkout/', views.checkout, name="checkout"),
    path('confirmation/', views.confirmation, name="confirmation"),
]
