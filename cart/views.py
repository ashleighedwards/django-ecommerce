from django.shortcuts import redirect, render
from django.contrib import messages
from decimal import Decimal
from orders.models import Order, OrderItem  # import from orders app
from store.models import Product

def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('product_list')

    # Create a new order
    order = Order.objects.create(total=0)

    total = Decimal(0)
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            subtotal=subtotal
        )
        total += subtotal

    order.total = total
    order.save()

    # Clear cart
    request.session['cart'] = {}
    request.session.modified = True

    messages.success(request, f"Order #{order.id} placed successfully!")
    return redirect('orders:order_list')  # use namespaced URL

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1  # subtract 1
        else:
            del cart[product_id_str]  # remove if 1

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart:cart_view')