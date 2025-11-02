from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart_view'),                 # Display the cart
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove 1 quantity
    path('checkout/', views.checkout, name='checkout'),         # Checkout and create an order
]
