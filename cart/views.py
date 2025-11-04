import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from decimal import Decimal

from accounts.forms import UserForm, ProfileForm
from accounts.models import Profile
from orders.models import Order, OrderItem
from store.models import Product
from django.db import transaction

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    profile, created = Profile.objects.get_or_create(user=request.user)

    user_form = UserForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, instance=profile)

    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:product_list')

    products = Product.objects.filter(id__in=cart.keys())
    total = sum(product.price * cart[str(product.id)] for product in products)
    amount_pence = int(total * Decimal('100'))

    profile_complete = all([request.user.email, profile.full_name, profile.address])

    if request.method == 'POST':
        # First, save forms if profile is incomplete
        if not profile_complete:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                profile_complete = True
            else:
                return render(request, 'cart/test_payment.html', {
                    'total': total,
                    'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'profile_complete': profile_complete
                })

        # Then, create Stripe PaymentIntent only if profile is complete
        if profile_complete:
            intent = stripe.PaymentIntent.create(
                amount=amount_pence,
                currency='gbp',
                payment_method_types=['card'],
            )
            return JsonResponse({'client_secret': intent.client_secret})

    return render(request, 'cart/test_payment.html', {
        'total': total,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_complete': profile_complete
    })

@transaction.atomic
def payment_success(request):
    if not request.user.is_authenticated:
        # Optionally redirect or raise an error if payment success is hit without a user
        return redirect('accounts:login')  # adjust to your login URL

    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:product_list')

    profile, created = Profile.objects.get_or_create(user=request.user)

    products = Product.objects.filter(id__in=cart.keys())
    total = sum(product.price * cart[str(product.id)] for product in products)

    order = Order.objects.create(
        user=request.user,
        total=total,
        full_name=profile.full_name,
        email=request.user.email,
        address=profile.address
    )

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