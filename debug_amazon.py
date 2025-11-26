import requests
from bs4 import BeautifulSoup
import urllib.parse
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

def get_headers(url=None):
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
    }
    return headers

query = "CMF by Nothing Buds 2a"
encoded_query = urllib.parse.quote(query)
url = f"https://www.amazon.in/s?k={encoded_query}"

print(f"Fetching: {url}")
headers = get_headers(url)

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML for inspection
        with open('amazon_search.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Saved to amazon_search.html")
        
        # Amazon search results
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        print(f"\nFound {len(items)} items with data-component-type='s-search-result'")
        
        if items:
            for i, item in enumerate(items[:3]):
                print(f"\n--- Item {i+1} ---")
                
                # Title
                title_tag = item.find('span', class_='a-text-normal')
                if title_tag:
                    print(f"Title: {title_tag.text.strip()[:60]}")
                else:
                    print("Title: NOT FOUND")
                
                # Price
                price_tag = item.find('span', class_='a-price-whole')
                if price_tag:
                    print(f"Price: {price_tag.text.strip()}")
                else:
                    print("Price: NOT FOUND")
                
                # Link
                link_tag = item.find('a', class_='a-link-normal')
                if link_tag:
                    print(f"Link: {link_tag.get('href', 'NO HREF')[:60]}")
                else:
                    print("Link: NOT FOUND")
        else:
            print("\nNo items found. Checking for alternative structures...")
            # Try other selectors
            alt_items = soup.find_all('div', {'data-index': True})
            print(f"Found {len(alt_items)} items with data-index attribute")
            
            # Check for CAPTCHA
            if 'Robot Check' in soup.title.string if soup.title else '':
                print("⚠️  CAPTCHA detected!")
except Exception as e:
    print(f"Error: {e}")
