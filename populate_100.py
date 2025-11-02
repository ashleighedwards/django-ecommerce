"""
This script populates the store app with 100 sample products.
Run it using:
    python3 manage.py shell < populate_100_products.py
"""

import random
from faker import Faker

# Django setup
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product  # Import your Product model

fake = Faker()  # Faker will generate random words/sentences

NUM_PRODUCTS = 100  # Number of products to create

# Optional: clear existing products so you start fresh
Product.objects.all().delete()

for _ in range(NUM_PRODUCTS):
    # Generate a random product name
    name = fake.unique.word().capitalize() + " " + random.choice(
        ["T-Shirt", "Jeans", "Sneakers", "Hat", "Jacket", "Bag", "Socks"]
    )

    # Generate a random short description
    description = fake.sentence(nb_words=10)

    # Generate a random price between $5 and $200
    price = round(random.uniform(5.0, 200.0), 2)

    # Save the product to the database
    Product.objects.create(
        name=name,
        description=description,
        price=price
    )

print(f"{NUM_PRODUCTS} products created successfully!")
