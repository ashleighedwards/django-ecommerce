from django.db import models

# Each model represents a database table.
# Django automatically creates a table for this class in the database.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Optional image field to store product images
    # 'upload_to' defines the folder inside MEDIA_ROOT where images will be saved
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    # Automatically stores the date/time when a product is first created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
