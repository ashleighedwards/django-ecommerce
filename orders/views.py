from django.shortcuts import render
from .models import Order

def order_list(request):
    orders = Order.objects.prefetch_related('items').all().order_by('-created_at')
    return render(request, 'orders/orders.html', {'orders': orders})
