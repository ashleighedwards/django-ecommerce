from django.contrib import admin
from .models import Product

# Register the Product model so it shows up in Django's admin dashboard.
admin.site.register(Product)