import requests
from bs4 import BeautifulSoup
import re
import json
import random

def get_headers(url=None):
    headers = {
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
    }
    return headers

query = "CMF by Nothing Buds 2a"
import urllib.parse
encoded_query = urllib.parse.quote(query)
url = f"https://www.flipkart.com/search?q={encoded_query}"

print(f"Fetching: {url}")
response = requests.get(url, headers=get_headers(url), timeout=10)
print(f"Status: {response.status_code}\n")

soup = BeautifulSoup(response.content, 'html.parser')

# Find JSON
scripts = soup.find_all('script')
json_data = None

for script in scripts:
    if script.string and 'window.__INITIAL_STATE__' in script.string:
        match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*});', script.string)
        if match:
            try:
                json_data = json.loads(match.group(1))
                break
            except:
                pass

if json_data:
    slots = json_data.get('multiWidgetState', {}).get('widgetsData', {}).get('slots', [])
    print(f"Found {len(slots)} slots\n")
    
    for i, slot in enumerate(slots):
        try:
            widget = slot.get('slotData', {}).get('widget', {})
            products = widget.get('data', {}).get('products', [])
            
            if products:
                print(f"=== Slot {i}: {len(products)} products ===")
                for j, prod in enumerate(products[:2]):
                    product_info = prod.get('productInfo', {}).get('value', {})
                    
                    # Title
                    titles = product_info.get('titles', {})
                    title = titles.get('title') or titles.get('newTitle')
                    print(f"\nProduct {j+1}: {title}")
                    
                    # URL
                    action = prod.get('productInfo', {}).get('action', {})
                    url = action.get('url')
                    print(f"URL: {url}")
                    
                    # Pricing - Show EVERYTHING
                    pricing = product_info.get('pricing', {})
                    print("Pricing keys:", list(pricing.keys()))
                    
                    # Try to get price from finalPrice
                    final_price = pricing.get('finalPrice', {})
                    print(f"finalPrice: {final_price}")
                    
                    # Try to get prices array
                    prices = pricing.get('prices', [])
                    if prices:
                        print(f"prices array ({len(prices)} items):")
                        for p in prices:
                            print(f"  - {p}")
                    
                    # Look for priceDisplayPrimary
                    pri_display = pricing.get('priceDisplayPrimary', {})
                    if pri_display:
                        print(f"priceDisplayPrimary: {pri_display}")
                    
                    print()
                print()
        except Exception as e:
            pass
else:
    print("No JSON data found")
