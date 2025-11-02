import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from decimal import Decimal
from orders.models import Order, OrderItem
from store.models import Product
from django.db import transaction

stripe.api_key = settings.STRIPE_SECRET_KEY

# Wrap checkout in a transaction so all DB writes happen together
# If something fails mid-way, Django rolls everything back automatically
@transaction.atomic
def checkout(request):
    #get cart data from session (session is per-user, per-browser)
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('store:product_list')

    #create a new order
    order = Order.objects.create(total=0)
    total = Decimal(0)

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        product.stock = max(product.stock - quantity, 0)
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

def test_payment(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:product_list')

    products = Product.objects.filter(id__in=cart.keys())
    total = sum(product.price * cart[str(product.id)] for product in products)
    amount_pence = int(total * 100)

    if request.method == 'POST':
        intent = stripe.PaymentIntent.create(
            amount=amount_pence,
            currency='gbp',
            payment_method_types=['card'],
        )
        return JsonResponse({'client_secret': intent.client_secret})

    return render(request, 'cart/test_payment.html', {
        'total': total,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })

@transaction.atomic
def payment_success(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:product_list')

    products = Product.objects.filter(id__in=cart.keys())
    total = sum(product.price * cart[str(product.id)] for product in products)

    order = Order.objects.create(total=total)

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity

        product.stock = max(product.stock - quantity, 0)
        product.save()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            subtotal=subtotal
        )

    request.session['cart'] = {}
    request.session.modified = True

    return render(request, 'cart/payment_success.html', {'order': order})