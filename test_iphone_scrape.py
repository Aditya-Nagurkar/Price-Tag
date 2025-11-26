import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_tracker.settings')
    django.setup()

from tracker.scraper import get_product_details

url = "https://www.flipkart.com/apple-iphone-15-blue-128-gb/p/itmbf14ef54f645d?pid=MOBGTAGPAQNVFZZY"

print(f"Testing URL: {url}\n")
details = get_product_details(url)

print("Results:")
print(f"  Title: {details.get('title')}")
print(f"  Price: {details.get('price')}")
print(f"  Currency: {details.get('currency')}")
print(f"  Error: {details.get('error')}")
