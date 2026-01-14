from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
import stripe
from .models import Order, OrderLineItem
from services.models import Service


stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """Checkout page"""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, 'Your cart is empty')
        return redirect('services')
    
    cart_items = []
    total = 0
    
    for service_id, quantity in cart.items():
        service = Service.objects.get(id=service_id)
        item_total = float(service.price) * quantity
        cart_items.append({
            'service': service,
            'quantity': quantity,
            'item_total': item_total,
        })
        total += item_total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """Success page after payment"""
    order = get_object_or_404(Order, order_number=order_number)
    
    if 'cart' in request.session:
        del request.session['cart']
    
    context = {
        'order': order,
    }
    return render(request, 'checkout/checkout_success.html', context)
