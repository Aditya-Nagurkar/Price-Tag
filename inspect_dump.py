from bs4 import BeautifulSoup
import re

with open('flipkart_dump.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find the specific text node
target_text = "Buds 2a"
matches = soup.find_all(string=re.compile(re.escape(target_text), re.IGNORECASE))

print(f"Found {len(matches)} matches for '{target_text}'")

for i, match in enumerate(matches):
    print(f"\nMatch {i}:")
    print(f"Text: {match.strip()}")
    
    # Walk up and print hierarchy
    parent = match.parent
    if parent.name in ['script', 'style', 'title']: continue
    
    print(f"\nMatch {i}:")
    print(f"Text: {match.strip()}")
    
    print("Hierarchy:")
    curr = parent
    for _ in range(10):
        if not curr: break
        attrs = curr.attrs
        cls = attrs.get('class', [])
        print(f"  <{curr.name} class='{cls}'>")
        
        # Check for link
        if curr.name == 'a':
            print(f"    -> LINK FOUND: {curr.get('href')}")
            
        # Check for price in this container
        price = curr.find(string=re.compile(r"₹"))
        if price:
            print(f"    -> Price in container: {price.strip()}")
            
        curr = curr.parent
