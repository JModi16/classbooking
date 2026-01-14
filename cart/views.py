from django.shortcuts import render
from django.http import JsonResponse
from services.models import Service


def view_cart(request):
    """Display shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for service_id, quantity in cart.items():
        try:
            service = Service.objects.get(id=service_id)
            item_total = float(service.price) * quantity
            cart_items.append({
                'service': service,
                'quantity': quantity,
                'item_total': item_total,
            })
            total += item_total
        except Service.DoesNotExist:
            pass
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, service_id):
    """Add service to cart"""
    cart = request.session.get('cart', {})
    service_id = str(service_id)
    
    if service_id in cart:
        cart[service_id] += 1
    else:
        cart[service_id] = 1
    
    request.session['cart'] = cart
    return JsonResponse({'success': True, 'cart_count': sum(cart.values())})


def remove_from_cart(request, service_id):
    """Remove service from cart"""
    cart = request.session.get('cart', {})
    service_id = str(service_id)
    
    if service_id in cart:
        del cart[service_id]
    
    request.session['cart'] = cart
    return JsonResponse({'success': True})
