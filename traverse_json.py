import json

with open('flipkart_data.json', 'r') as f:
    data = json.load(f)

def find_keys(obj, target_keys, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in target_keys:
                print(f"Found '{k}' at {path}.{k}")
                # Print a sample of the value if it's a list
                if isinstance(v, list) and len(v) > 0:
                    print(f"  Sample item keys: {v[0].keys() if isinstance(v[0], dict) else 'Not dict'}")
            
            find_keys(v, target_keys, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            find_keys(item, target_keys, f"{path}[{i}]")

print("Searching for 'slots', 'products', 'widget'...")
find_keys(data, ['slots', 'products', 'widget'])
