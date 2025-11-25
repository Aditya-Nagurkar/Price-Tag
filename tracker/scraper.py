import requests
from bs4 import BeautifulSoup
import random
import re
import json

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
]

BLACKLIST_TITLES = [
    "Add to your order",
    "Amazon.in",
    "Amazon.com",
    "Shopping Cart",
    "Page Not Found",
    "Robot Check",
    "Welcome to Amazon",
]

def get_headers():
    # More realistic headers to avoid bot detection
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Connection': 'keep-alive',
    }

def clean_price(price_str):
    if not price_str:
        return None, '$'
    
    price_str = str(price_str).strip()
    
    # Extract currency symbol
    currency = '$'
    # Common symbols
    if '₹' in price_str: currency = '₹'
    elif '€' in price_str: currency = '€'
    elif '£' in price_str: currency = '£'
    elif '¥' in price_str: currency = '¥'
    
    # Remove common currency symbols and whitespace
    price_str = re.sub(r'[^\d.,]', '', price_str)
    
    # Handle cases like 1,299.00 or 1.299,00
    if ',' in price_str and '.' in price_str:
        if price_str.find(',') < price_str.find('.'):
            # 1,299.00 format
            price_str = price_str.replace(',', '')
        else:
            # 1.299,00 format
            price_str = price_str.replace('.', '').replace(',', '.')
    elif ',' in price_str:
        # 1,299 format (assuming comma is thousands separator if no decimal)
        price_str = price_str.replace(',', '')
        
    try:
        return float(price_str), currency
    except ValueError:
        return None, '$'

def get_product_details(url):
    session = requests.Session()
    try:
        # Use session for cookie handling
        response = session.get(url, headers=get_headers(), timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for CAPTCHA
        if "Robot Check" in soup.title.string if soup.title else "" or "captcha" in response.url.lower():
            return {'title': None, 'price': None, 'currency': '$', 'image_url': None, 'error': "Amazon CAPTCHA detected. Try again later."}

        title = None
        price = None
        currency = '$'
        image_url = None

        # --- Amazon Specific Logic ---
        # Check both input URL and final URL (in case of redirects/short links)
        if 'amazon' in url or 'amzn' in url or 'amazon' in response.url:
            # Title Strategies
            title_selectors = [
                'productTitle', 
                'title', 
                'ebooksProductTitle'
            ]
            for selector in title_selectors:
                t = soup.find(id=selector)
                if t:
                    candidate_title = t.get_text().strip()
                    if candidate_title and candidate_title not in BLACKLIST_TITLES:
                        title = candidate_title
                        break
            
            # Image Extraction Strategy
            # 1. Check for data-a-dynamic-image in common IDs
            img_candidates = ['landingImage', 'imgBlkFront', 'main-image', 'ebooksImgBlkFront']
            for img_id in img_candidates:
                img_tag = soup.find('img', id=img_id)
                if img_tag:
                    # Try to parse the dynamic image JSON
                    dynamic_data = img_tag.get('data-a-dynamic-image')
                    if dynamic_data:
                        try:
                            # It's a JSON string like {"url":[w,h], ...}
                            # We want the largest one (or just the first one)
                            images_dict = json.loads(dynamic_data)
                            if images_dict:
                                # Get the first URL (keys are URLs)
                                image_url = list(images_dict.keys())[0]
                                break
                        except json.JSONDecodeError:
                            pass
                    
                    # Fallback to data-old-hires or src
                    if not image_url:
                        image_url = img_tag.get('data-old-hires') or img_tag.get('src')
                    
                    if image_url:
                        break
            
            # 2. Try dynamic image wrapper if ID lookup failed
            if not image_url:
                dynamic_img = soup.find('div', id='imgTagWrapperId')
                if dynamic_img:
                    img_tag = dynamic_img.find('img')
                    if img_tag:
                         # Try dynamic data here too
                        dynamic_data = img_tag.get('data-a-dynamic-image')
                        if dynamic_data:
                            try:
                                images_dict = json.loads(dynamic_data)
                                if images_dict:
                                    image_url = list(images_dict.keys())[0]
                            except:
                                pass
                        
                        if not image_url:
                            image_url = img_tag.get('src')
            
            # 3. Try finding the main image by class if IDs fail
            if not image_url:
                main_img_class = soup.find('img', class_='a-dynamic-image')
                if main_img_class:
                    image_url = main_img_class.get('src')

        # --- Generic Logic (Fallback) ---
        
        # Title Fallback
        if not title or title in BLACKLIST_TITLES:
            meta_title = soup.find('meta', property='og:title')
            if meta_title:
                title = meta_title['content']
            
            if not title or title in BLACKLIST_TITLES:
                 if soup.title:
                    title = soup.title.string.strip()
            
            if not title or title in BLACKLIST_TITLES:
                h1 = soup.find('h1')
                if h1:
                    title = h1.get_text().strip()
        
        # Clean title if it still contains bad strings (sometimes "Amazon.in: ...")
        if title:
            for bad in BLACKLIST_TITLES:
                if title == bad:
                    title = None
                    break

        # Priority 1: Meta tags (most reliable)
        price_meta_properties = [
            'product:price:amount',
            'og:price:amount',
            'price',
        ]
        
        for prop in price_meta_properties:
            meta_price = soup.find('meta', property=prop) or soup.find('meta', attrs={'name': prop})
            if meta_price:
                cleaned, detected_currency = clean_price(meta_price.get('content'))
                if cleaned:
                    price = cleaned
                    currency = detected_currency
                    break
        
        # Priority 2: Common price classes/IDs if meta failed
        if not price:
            # Regex for currency symbols followed by digits
            # Supports $, ₹, €, £
            price_regex = re.compile(r'[₹$€£]\s*[\d,.]+')
            
            # Search in specific price classes first
            price_classes = [
                'a-price-whole', 'a-offscreen', # Amazon
                'price', 'current-price', 'amount', # Generic
                '_30jeq3', # Flipkart
            ]
            
            for cls in price_classes:
                element = soup.find(class_=cls)
                if element:
                    # For Amazon 'a-price-whole', it might be just "1,299" without symbol
                    text = element.get_text().strip()
                    # If it's just digits and separators, assume it's the price
                    if re.match(r'^[\d,.]+$', text):
                         cleaned, _ = clean_price(text) # Currency might be missing here, default to $ or previous detection
                         if cleaned:
                             price = cleaned
                             # If we found a price but no currency yet, try to find a symbol nearby
                             if 'amazon' in url: # Amazon usually implies local currency if not specified, or we can look for symbol
                                 symbol_span = element.find_previous(class_='a-price-symbol')
                                 if symbol_span:
                                     currency = symbol_span.get_text().strip()
                             elif 'flipkart' in url:
                                 currency = '₹' # Flipkart is mostly India
                             break
                    
                    match = price_regex.search(text)
                    if match:
                        cleaned, detected_currency = clean_price(match.group())
                        if cleaned:
                            price = cleaned
                            currency = detected_currency
                            break
                if price: break

        # Standard meta tag extraction (fallback for Amazon, primary for others)
        if not image_url:
            meta_image = soup.find('meta', property='og:image')
            if meta_image:
                image_url = meta_image.get('content')
        
        if not image_url:
            # Fallback to first large image
            images = soup.find_all('img')
            for img in images:
                src = img.get('src', '')
                if src.startswith('http') and 'logo' not in src.lower() and 'icon' not in src.lower() and 'sprite' not in src.lower():
                    image_url = src
                    break

        return {
            'title': title,
            'price': price,
            'currency': currency,
            'image_url': image_url,
            'error': None
        }

    except Exception as e:
        return {
            'title': None,
            'price': None,
            'currency': '$',
            'image_url': None,
            'error': str(e)
        }
