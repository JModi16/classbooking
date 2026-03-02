from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_http_methods
import stripe
import uuid
from .models import ClassBooking
from services.models import ExerciseClass


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
@require_http_methods(["GET", "POST"])
def checkout(request):
    """Checkout page for class bookings"""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, 'Your cart is empty')
        return redirect('classes')
    
    # Build cart items with availability check
    cart_items = []
    total = 0
    
    for class_id, quantity in cart.items():
        try:
            exercise_class = ExerciseClass.objects.get(id=class_id)
            
            # Verify quantity doesn't exceed available spots
            available_spots = exercise_class.get_available_spots()
            if int(quantity) > available_spots:
                messages.warning(request, f'{exercise_class.name}: Only {available_spots} spot(s) available')
                continue
            
            item_total = float(exercise_class.price) * int(quantity)
            cart_items.append({
                'exercise_class': exercise_class,
                'quantity': int(quantity),
                'item_total': item_total,
            })
            total += item_total
        except ExerciseClass.DoesNotExist:
            messages.warning(request, 'One or more classes no longer exist')
            continue
    
    if not cart_items:
        messages.error(request, 'No valid items in cart')
        return redirect('view_cart')
    
    # Apply delivery threshold logic if applicable
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
    else:
        delivery = 0
    
    grand_total = total + delivery
    
    # Stripe amount in pence
    stripe_total = round(grand_total * 100)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': 'test_secret',  # This will be set via AJAX
    }
    
    return render(request, 'checkout/checkout.html', context)


@login_required
def checkout_success(request, booking_id):
    """Success page after payment"""
    booking = get_object_or_404(ClassBooking, booking_id=booking_id, user=request.user)
    
    if 'cart' in request.session:
        del request.session['cart']
    
    context = {
        'booking': booking,
    }
    return render(request, 'checkout/checkout_success.html', context)
    return render(request, 'checkout/checkout_success.html', context)
