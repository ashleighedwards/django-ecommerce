from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

# This view fetches all products from the database and sends them to a template
def product_list(request):
    # Get all Product objects
    products = Product.objects.all()

    # Render the 'store/product_list.html' template
    # Pass the products as a context dictionary
    return render(request, 'store/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get cart from session, or create if it doesn't exist
    cart = request.session.get('cart', {})

    # Add product or increase quantity
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    # Save back to session
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('store:product_list')  # or redirect to cart page


