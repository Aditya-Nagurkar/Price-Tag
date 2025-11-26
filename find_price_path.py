import json

with open('current_state.json', 'r') as f:
    data = json.load(f)

def find_path(obj, target_key, target_value, path=""):
    """Recursively find paths to matching key-value pairs"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_path = f"{path}.{k}" if path else k
            if k == target_key and v == target_value:
                print(f"Found at: {new_path}")
                # Print parent context
                print(f"  Full path context needed")
                return new_path
            result = find_path(v, target_key, target_value, new_path)
            if result:
                return result
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_path = f"{path}[{i}]"
            result = find_path(item, target_key, target_value, new_path)
            if result:
                return result
    return None

print("Searching for displayPrice = 1899...")
path = find_path(data, 'displayPrice', 1899)

if path:
    print(f"\nPath: {path}")
    
    # Now let's trace back to find the parent product structure
    print("\n--- Checking parent structure ---")
    parts = path.split('.')
    
    # Get to the product level (usually a few levels up from pricing)
    for i in range(len(parts) - 1, 0, -1):
        parent_path = '.'.join(parts[:i])
        print(f"\nParent path: {parent_path}")
        
        # Try to access this path
        obj = data
        for part in parts[:i]:
            if '[' in part:
                key = part.split('[')[0]
                idx = int(part.split('[')[1].rstrip(']'))
                obj = obj[key][idx]
            else:
                obj = obj.get(part, {})
        
        if isinstance(obj, dict):
            keys = list(obj.keys())
            print(f"  Keys: {keys[:10]}")  # Show first 10 keys
            
            # Check for common product fields
            if any(k in keys for k in ['productInfo', 'value', 'titles', 'pricing']):
                print("  ^ This level has product-like structure")
                
                # Check what's directly accessible
                if 'pricing' in keys:
                    pricing = obj.get('pricing', {})
                    print(f"  Direct pricing access: {list(pricing.keys())}")
