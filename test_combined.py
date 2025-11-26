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

if __name__ == "__main__":
    query = "CMF by Nothing Buds 2a"
    print(f"Testing search_products (combined) with query: '{query}'\n")
    results = search_products(query)
    
    print(f"Found {len(results)} total results:\n")
    
    # Group by source
    amazon_results = [r for r in results if r['source'] == 'Amazon']
    flipkart_results = [r for r in results if r['source'] == 'Flipkart']
    
    print(f"Amazon: {len(amazon_results)} results")
    print(f"Flipkart: {len(flipkart_results)} results")
    print()
    
    for i, res in enumerate(results):
        print(f"Result {i+1} ({res['source']}):")
        print(f"  Title: {res['title'][:60]}")
        print(f"  Price: {res['currency']}{res['price']}")
        print()
