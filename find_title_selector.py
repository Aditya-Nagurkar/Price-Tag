from bs4 import BeautifulSoup

with open('amazon_search.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Get first search result
items = soup.find_all('div', {'data-component-type': 's-search-result'})
if items:
    first_item = items[2]  # Get 3rd item (often more reliable than first which may be sponsored)
    
    print("=== Searching for title in item ===")
    
    # Try different selectors
    selectors = [
        ('span.a-text-normal', 'span', 'a-text-normal'),
        ('h2 span', 'h2', None),
        ('h2.a-size-mini span', 'h2', 'a-size-mini'),
        ('h2.a-size-base-plus', 'h2', 'a-size-base-plus'),
        ('.a-size-base-plus', None, 'a-size-base-plus'),
        ('.a-size-medium', None, 'a-size-medium'),
    ]
    
    for desc, tag, cls in selectors:
        if tag and cls:
            result = first_item.find(tag, class_=cls)
        elif tag:
            result = first_item.find(tag)
        elif cls:
            result = first_item.find(class_=cls)
        
        if result:
            text = result.get_text().strip()
            if len(text) > 10:  # Likely a title if longer than 10 chars
                print(f"✓ Found with {desc}: {text[:60]}")
            
    # Also try finding all spans and checking their content
    print("\n=== All span tags with text > 20 chars ===")
    spans = first_item.find_all('span')
    for i, span in enumerate(spans):
        text = span.get_text().strip()
        if len(text) > 20 and 'CMF' in text:
            classes = span.get('class', [])
            print(f"Span {i}: classes={classes}")
            print(f"  Text: {text[:80]}")
