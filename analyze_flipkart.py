from bs4 import BeautifulSoup
import re

def analyze_html():
    with open('debug_flipkart_search.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all elements containing "Buds 2a" (shorter query to match variations)
    # Exclude head/title
    body = soup.find('body')
    if not body:
        print("No body tag found!")
        return

    target_text = re.compile(r"Buds 2a", re.IGNORECASE)
    
    # Find text nodes
    results = body.find_all(string=target_text)
    
    print(f"Found {len(results)} matches in body.")
    
    for i, res in enumerate(results):
        parent = res.parent
        if parent.name in ['script', 'style']:
            continue
            
        print(f"\nMatch {i+1}: {res.strip()[:50]}...")
        print(f"Tag: {parent.name}, Classes: {parent.get('class')}")
        
        # Walk up to find a container with a class
        curr = parent
        for _ in range(5):
            curr = curr.parent
            if curr and curr.get('class'):
                print(f"  Ancestor: {curr.name} class={curr.get('class')}")
                
                # Check if this ancestor contains a price
                price_text = curr.find(string=re.compile(r"₹"))
                if price_text:
                    print(f"    -> Contains price: {price_text.strip()}")
                    print(f"    -> Price tag: {price_text.parent.name} class={price_text.parent.get('class')}")

analyze_html()
