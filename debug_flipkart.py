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

from tracker.scraper import search_flipkart

if __name__ == "__main__":
    query = "CMF by Nothing Buds 2a"
    print(f"Testing search_flipkart with query: '{query}'")
    results = search_flipkart(query)
    
    print(f"\nFound {len(results)} results:")
    for i, res in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"  Title: {res['title']}")
        print(f"  Price: {res['currency']}{res['price']}")
        print(f"  Source: {res['source']}")
        print(f"  URL: {res['url']}")
