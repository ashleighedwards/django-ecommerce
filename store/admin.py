from django.contrib import admin
from .models import Product

#register the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'price', 'stock', 'description')
    list_editable = ('price','stock',)
    search_fields = ('name',)
