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

print(f"Fetching: {url}\n")
response = requests.get(url, headers=get_headers(url), timeout=10)

soup = BeautifulSoup(response.content, 'html.parser')

# Save HTML for inspection
with open('current_flipkart.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
print("Saved to current_flipkart.html")

# Find JSON
scripts = soup.find_all('script')
json_data = None

for script in scripts:
    if script.string and 'window.__INITIAL_STATE__' in script.string:
        match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*});', script.string)
        if match:
            try:
                json_data = json.loads(match.group(1))
                with open('current_state.json', 'w') as f:
                    json.dump(json_data, f, indent=2)
                print("Saved to current_state.json\n")
                break
            except:
                pass

# Now search for any text containing "1899" or "2499" in the HTML
print("Searching HTML for price patterns...")
if '1899' in response.text:
    print("✓ Found '1899' in HTML")
if '2499' in response.text:
    print("✓ Found '2499' in HTML")

# Search in JSON for these prices
if json_data:
    json_str = json.dumps(json_data)
    if '1899' in json_str:
        print("✓ Found '1899' in JSON")
    if '2499' in json_str:
        print("✓ Found '2499' in JSON")
