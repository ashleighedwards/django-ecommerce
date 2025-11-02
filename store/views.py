from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

#this view fetches all products from the database and sends them to a template
def product_list(request):
    # Get all Product objects
    products = Product.objects.all()

    #render the product list template
    #pass the products as a context dictionary
    return render(request, 'store/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        return JsonResponse({'error': f"'{product.name}' is out of stock."}, status=400)

    #get cart from session, or create if it doesn't exist
    cart = request.session.get('cart', {})

    #add product or increase quantity
    if str(product_id) in cart:
        if cart[str(product_id)] < product.stock:
            cart[str(product_id)] += 1
        else:
            return JsonResponse({'error': "Reached maximum available stock."}, status=400)
    else:
        cart[str(product_id)] = 1

    #save back to session
    request.session['cart'] = cart
    request.session.modified = True

    return JsonResponse({
        'message': f"Added {product.name} to your cart.",
        'cart_count': sum(cart.values())
    })


