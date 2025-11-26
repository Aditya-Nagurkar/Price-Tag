from bs4 import BeautifulSoup
import json
import re

with open('flipkart_dump.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')

print(f"Found {len(scripts)} scripts")

for i, script in enumerate(scripts):
    if script.string:
        if "CMF" in script.string:
            print(f"\nScript {i} contains 'CMF':")
            # Try to find JSON object assignment
            # Look for window.__INITIAL_STATE__ = { ... } or similar
            match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*});', script.string)
            if match:
                print("  Found window.__INITIAL_STATE__")
                try:
                    data = json.loads(match.group(1))
                    print("  Successfully parsed JSON")
                    # Save to file for inspection
                    with open('flipkart_data.json', 'w') as f:
                        json.dump(data, f, indent=2)
                    print("  Saved to flipkart_data.json")
                except:
                    print("  Failed to parse JSON")
            else:
                print("  No standard state assignment found")
                print(f"  Snippet: {script.string[:100]}...")
