import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_tracker.settings')
    django.setup()

from tracker.scraper import search_products

# Test 1: Amazon product - should only search Flipkart
print("=" * 60)
print("Test 1: Exclude Amazon (as if product is from Amazon)")
print("=" * 60)
query = "CMF by Nothing Buds 2a"
results = search_products(query, exclude_source='amazon')

print(f"\nQuery: '{query}'")
print(f"Exclude: Amazon")
print(f"Found {len(results)} results:\n")

for i, res in enumerate(results):
    print(f"{i+1}. [{res['source']}] {res['title'][:50]} - ₹{res['price']}")

# Test 2: Flipkart product - should only search Amazon
print("\n" + "=" * 60)
print("Test 2: Exclude Flipkart (as if product is from Flipkart)")
print("=" * 60)

results = search_products(query, exclude_source='flipkart')

print(f"\nQuery: '{query}'")
print(f"Exclude: Flipkart")
print(f"Found {len(results)} results:\n")

for i, res in enumerate(results):
    print(f"{i+1}. [{res['source']}] {res['title'][:50]} - ₹{res['price']}")

# Test 3: No exclusion - should search both
print("\n" + "=" * 60)
print("Test 3: No exclusion (search all)")
print("=" * 60)

results = search_products(query, exclude_source=None)

print(f"\nQuery: '{query}'")
print(f"Exclude: None")
print(f"Found {len(results)} results:\n")

for i, res in enumerate(results):
    print(f"{i+1}. [{res['source']}] {res['title'][:50]} - ₹{res['price']}")
