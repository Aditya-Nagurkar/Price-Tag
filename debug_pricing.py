import json

with open('flipkart_data.json', 'r') as f:
    data = json.load(f)

try:
    slots = data['multiWidgetState']['widgetsData']['slots']
    
    for i, slot in enumerate(slots):
        try:
            products = slot['slotData']['widget']['data']['products']
            if products:
                # Check if first product has pricing data
                product_info = products[0].get('productInfo', {}).get('value', {})
                pricing = product_info.get('pricing', {})
                
                if pricing:  # Only print slots with pricing data
                    print(f"\n=== Slot {i} HAS PRICING DATA ===")
                    
                    # Title
                    titles = product_info.get('titles', {})
                    title = titles.get('title', 'N/A')
                    print(f"First product: {title[:60]}")
                    
                    # Show pricing structure
                    final_price = pricing.get('finalPrice', {})
                    price_val = final_price.get('value')
                    print(f"finalPrice.value = {price_val}")
                    
                    prices = pricing.get('prices', [])
                    print(f"Available prices:")
                    for p in prices:
                        print(f"  {p.get('name')}: {p.get('value')}")
                    print()
        except Exception as e:
            pass
except Exception as e:
    print(f"Error: {e}")
