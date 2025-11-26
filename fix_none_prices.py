"""
Quick script to manually update product prices that show None
Usage: python fix_none_prices.py
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__ )))

import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_tracker.settings')
    django.setup()

from tracker.models import Product
from tracker.scraper import get_product_details

# Find all products with None price
products_with_none = Product.objects.filter(current_price__isnull=True, is_active=True)

print(f"Found {products_with_none.count()} products with None price")

for product in products_with_none:
    print(f"\nUpdating: {product.name}")
    print(f"URL: {product.url}")
    
    details = get_product_details(product.url)
    
    if details['error']:
        print(f"  ❌ Error: {details['error']}")
    elif details['price']:
        product.current_price = details['price']
        product.save()
        print(f"  ✓ Updated price to: {details['currency']}{details['price']}")
    else:
        print(f"  ⚠ No price found")

print("\nDone!")
