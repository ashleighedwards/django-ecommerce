from django.urls import path
from . import views

app_name = 'store'
# Define URL patterns for this app.
# When a user visits the root path (""), Django runs views.product_list
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]