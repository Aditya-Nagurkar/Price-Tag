import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.parse

def get_headers(url=None):
    headers = {
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
    }
    return headers

query = "CMF by Nothing Buds 2a"
encoded_query = urllib.parse.quote(query)
url = f"https://www.flipkart.com/search?q={encoded_query}"

print(f"Fetching: {url}")
response = requests.get(url, headers=get_headers(url), timeout=10)

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
    
    for i, slot in enumerate(slots):
        try:
            widget = slot.get('slotData', {}).get('widget', {})
            products = widget.get('data', {}).get('products', [])
            
            if products and i == 6:  # Check slot 6
                print(f"=== Slot {i} - First Product Full Structure ===")
                print(json.dumps(products[0], indent=2)[:2000])
                print("\n\n...")
                break
        except Exception as e:
            pass
