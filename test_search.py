import requests
import sys
import os
from bs4 import BeautifulSoup
import urllib.parse

sys.path.append(os.getcwd())
from tracker.scraper import get_headers

def debug_search(site, url):
    print(f"Debugging {site}: {url}")
    headers = get_headers(url)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            filename = f"debug_{site}_search.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Saved HTML to {filename}")
            
            # Quick check for common elements
            soup = BeautifulSoup(response.content, 'html.parser')
            if site == 'flipkart':
                # Check for mobile classes
                print("Mobile classes check:")
                print(f"Found '._1AtVbE' (Desktop row): {len(soup.select('._1AtVbE'))}")
                print(f"Found '.cPHDOP' (Mobile container?): {len(soup.select('.cPHDOP'))}") 
                print(f"Found '._2kHMtA' (Old desktop): {len(soup.select('._2kHMtA'))}")
            elif site == 'amazon':
                print("Amazon classes check:")
                print(f"Found 's-search-result': {len(soup.find_all('div', {'data-component-type': 's-search-result'}))}")
                
    except Exception as e:
        print(f"Error: {e}")

query = "CMF by Nothing Buds 2a"

# Debug Flipkart
encoded_query = urllib.parse.quote(query)
debug_search('flipkart', f"https://www.flipkart.com/search?q={encoded_query}")

# Debug Amazon
debug_search('amazon', f"https://www.amazon.in/s?k={encoded_query}")
