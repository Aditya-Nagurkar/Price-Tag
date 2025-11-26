import json

with open('flipkart_data.json', 'r') as f:
    data = json.load(f)

try:
    # Try slot 6 first as seen in previous output
    products = data['multiWidgetState']['widgetsData']['slots'][6]['slotData']['widget']['data']['products']
    if products:
        print("Found products in slot 6")
        product = products[0]
        print("Title:", product['productInfo']['value']['titles']['title'])
        print("Pricing:", json.dumps(product['productInfo']['value']['pricing'], indent=2))
        print("URL:", product['productInfo']['action']['url'])
    else:
        print("No products in slot 6")
except Exception as e:
    print(f"Error accessing slot 6: {e}")
    
    # Try to find any product list
    print("\nSearching for any product list...")
    slots = data['multiWidgetState']['widgetsData']['slots']
    for i, slot in enumerate(slots):
        try:
            products = slot['slotData']['widget']['data']['products']
            if products:
                print(f"Found products in slot {i}")
                print(json.dumps(products[0], indent=2))
                break
        except:
            pass
