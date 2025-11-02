from django.core.paginator import Paginator
from django.db.models import Case, When, Value, BooleanField
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Product

#this view fetches all products from the database and sends them to a template
def product_list(request):
    sort = request.GET.get('sort', 'name')  # default sort by name

    products = Product.objects.annotate(
        is_out_of_stock=Case(
            When(stock__lte=0, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    )

    if sort == 'price_asc':
        products = products.order_by('is_out_of_stock', 'price')
    elif sort == 'price_desc':
        products = products.order_by('is_out_of_stock', '-price')
    elif sort == 'name_asc':
        products = products.order_by('is_out_of_stock', 'name')
    elif sort == 'name_desc':
        products = products.order_by('is_out_of_stock', '-name')
    else:
        products = products.order_by('is_out_of_stock', 'name')  # default

    #render the product list template
    #pass the products as a context dictionary
    paginator = Paginator(products, 36)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/product_list.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'current_sort': sort,
    })

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
        'cart_count': len(cart)
    })


