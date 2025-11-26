from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, PriceHistory
from .scraper import get_product_details
from django.utils import timezone

def dashboard(request):
    products = Product.objects.all().order_by('-created_at')
    total_items = products.count()
    deals_found = sum(1 for p in products if p.is_below_threshold)
    
    context = {
        'products': products,
        'total_items': total_items,
        'deals_found': deals_found,
    }
    return render(request, 'tracker/dashboard.html', context)

def add_product(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        target_price = request.POST.get('target_price')
        
        if url and target_price:
            try:
                target_price = float(target_price)
                details = get_product_details(url)
                
                if details['error']:
                    messages.error(request, f"Error scraping URL: {details['error']}")
                else:
                    product = Product.objects.create(
                        name=details['title'] or "Unknown Product",
                        url=url,
                        image_url=details.get('image_url'),
                        currency=details.get('currency', '₹'),
                        target_price=target_price,
                        current_price=details['price'],
                        last_checked=timezone.now() if details['price'] else None
                    )
                    
                    if details['price']:
                        PriceHistory.objects.create(
                            product=product,
                            price=details['price']
                        )
                    
                    messages.success(request, "Product added successfully!")
            except ValueError:
                messages.error(request, "Invalid target price.")
        else:
            messages.error(request, "Please fill in all fields.")
            
    return redirect('dashboard')

from django.core.mail import send_mail
from django.conf import settings

def update_prices(request):
    products = Product.objects.filter(is_active=True)
    updated_count = 0
    
    for product in products:
        details = get_product_details(product.url)
        if not details['error'] and details['price']:
            old_price = product.current_price
            product.current_price = details['price']
            if details.get('image_url'):
                product.image_url = details['image_url']
            
            if details.get('currency'):
                product.currency = details['currency']
            
            # Only update title if it's valid and not in blacklist
            new_title = details.get('title')
            BLACKLIST_TITLES = ["Add to your order", "Amazon.in", "Shopping Cart", "Page Not Found", "Unknown Product"]
            
            if new_title and new_title not in BLACKLIST_TITLES:
                product.name = new_title
                
            product.last_checked = timezone.now()
            product.save()
            
            PriceHistory.objects.create(
                product=product,
                price=details['price']
            )
            updated_count += 1
            
            # Check for price drop and send email
            # Check for price drop and send email
            if product.is_below_threshold:
                print(f"DEBUG: Product {product.name} is below threshold!")
                print(f"DEBUG: Current: {product.current_price}, Target: {product.target_price}")
                
                subject = f"Price Drop Alert: {product.name}"
                message = f"Good news! The price for {product.name} has dropped to {product.current_price}. This is below your target of {product.target_price}.\n\nCheck it out here: {product.url}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email] if request.user.is_authenticated else ['user@example.com']
                print(f"DEBUG: Sending email to {recipient_list}")
                
                try:
                    send_mail(subject, message, from_email, recipient_list)
                    print(f"DEBUG: Email sent successfully for {product.name}")
                except Exception as e:
                    print(f"DEBUG: Failed to send email: {e}")
            else:
                print(f"DEBUG: Product {product.name} is NOT below threshold. Current: {product.current_price}, Target: {product.target_price}")


        elif details['error']:
            messages.warning(request, f"Failed to update {product.name}: {details['error']}")
            
    if updated_count > 0:
        messages.success(request, f"Updated {updated_count} products.")
    elif not messages.get_messages(request):
        messages.info(request, "No products updated.")
        
    return redirect('dashboard')

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted.")
    return redirect('dashboard')

def get_price_history(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    history = product.price_history.all().order_by('timestamp')
    
    data = {
        'labels': [h.timestamp.strftime('%Y-%m-%d %H:%M:%S') for h in history],
        'prices': [float(h.price) for h in history],
        'currency': product.currency
    }
    
    from django.http import JsonResponse
    return JsonResponse(data)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Calculate Deal Score (0-100)
    # Logic: 
    # If current <= target, score is high (80-100)
    # If current > target, score drops
    deal_score = 0
    if product.current_price and product.target_price:
        ratio = float(product.target_price) / float(product.current_price)
        if ratio >= 1:
            # Good deal
            deal_score = min(100, 80 + (ratio - 1) * 100)
        else:
            # Bad deal
            deal_score = max(0, 80 - (1 - ratio) * 200)
            
    context = {
        'product': product,
        'deal_score': int(deal_score),
    }
    context = {
        'product': product,
        'deal_score': int(deal_score),
    }
    return render(request, 'tracker/product_detail.html', context)

from django.contrib.auth import login
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='tracker.backends.EmailBackend')
            
            # Send welcome email
            try:
                greeting_name = user.first_name if user.first_name else "there"
                send_mail(
                    'Welcome to PriceTag!',
                    f'Hi {greeting_name},\n\nThanks for signing up for PriceTag! You can now track product prices and get notified when they drop.\n\nHappy tracking!',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Failed to send welcome email: {e}")
                
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'tracker/signup.html', {'form': form})
