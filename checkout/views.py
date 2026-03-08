from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
import json
import uuid
import logging
from .models import ClassBooking, ClassBookingLineItem
from services.models import ExerciseClass

logger = logging.getLogger(__name__)


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
@require_http_methods(["GET", "POST"])
def checkout(request):
    """Checkout page for class bookings"""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, 'Your cart is empty')
        return redirect('classes')
    
    if request.method == 'POST':
        # Payment successful, get booking and redirect
        client_secret = request.POST.get('client_secret', '')
        pid = client_secret.split('_secret')[0]
        
        try:
            booking = ClassBooking.objects.get(stripe_pid=pid)
            # Clear cart
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True
            return redirect('checkout_success', booking_id=booking.booking_id)
        except ClassBooking.DoesNotExist:
            messages.error(request, 'Booking not found. Please contact support.')
            return redirect('view_cart')
    
    # GET request - Build cart items with availability check
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
    
    # Apply delivery threshold logic if applicable (set to 0 for class bookings)
    delivery = 0
    grand_total = total + delivery
    
    # Create Stripe Payment Intent
    stripe_total = round(grand_total * 100)  # Stripe expects amount in pence
    
    try:
        # Explicitly set and verify API key
        stripe.api_key = settings.STRIPE_SECRET_KEY
        logger.debug(f'Stripe API Key before Payment Intent: {stripe.api_key[:20]}...')
        logger.debug(f'Stripe Currency: {settings.STRIPE_CURRENCY}')
        logger.debug(f'Stripe Amount (pence): {stripe_total}')
        
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                'username': request.user.username,
                'cart': json.dumps(cart),
            }
        )
        logger.debug(f'Payment Intent created successfully: {intent.id}')
    except Exception as e:
        logger.error(f'Stripe API Error - Type: {type(e).__name__}, Message: {str(e)}, ApiKey set: {bool(stripe.api_key)}')
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('view_cart')
    
    # Show checkout form
    context = {
        'cart_items': cart_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }
    
    return render(request, 'checkout/checkout.html', context)


@require_POST
@login_required
def cache_checkout_data(request):
    """Cache checkout data and create pending booking"""
    try:
        # Get client_secret from POST data
        client_secret = request.POST.get('client_secret')
        if not client_secret:
            # Try JSON body for backwards compatibility
            try:
                data = json.loads(request.body)
                client_secret = data.get('client_secret')
            except:
                pass
        
        if not client_secret:
            return JsonResponse({'error': 'Missing client secret'}, status=400)
            
        pid = client_secret.split('_secret')[0]
        cart = request.session.get('cart', {})
        
        # Get cart items and create booking
        cart_items = []
        total = 0
        for class_id, quantity in cart.items():
            exercise_class = ExerciseClass.objects.get(id=class_id)
            item_total = float(exercise_class.price) * int(quantity)
            cart_items.append({
                'exercise_class': exercise_class,
                'quantity': int(quantity),
                'item_total': item_total,
            })
            total += item_total
        
        # Create booking with pending status
        booking = ClassBooking.objects.create(
            booking_id=str(uuid.uuid4()),
            user=request.user,
            course=cart_items[0]['exercise_class'],
            full_name=request.user.get_full_name() or request.user.username,
            email=request.user.email,
            status='pending',
            payment_status='unpaid',
            total_amount=total,
            stripe_pid=pid,
        )
        
        # Create line items
        for item in cart_items:
            ClassBookingLineItem.objects.create(
                booking=booking,
                item_type='class',
                description=item['exercise_class'].name,
                quantity=item['quantity'],
                unit_price=item['exercise_class'].price,
            )
        
        # Update Payment Intent metadata
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(cart),
            'username': request.user.username,
            'user_id': request.user.id,
            'booking_id': str(booking.booking_id),
        })
        
        return JsonResponse({'success': True, 'booking_id': str(booking.booking_id)})
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def checkout_success(request, booking_id):
    """Success page after payment confirmation"""
    booking = get_object_or_404(ClassBooking, booking_id=booking_id, user=request.user)
    
    # Clear the cart
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
    
    messages.success(request, f'Booking confirmed! Your booking ID is {booking_id}')
    
    context = {
        'booking': booking,
    }
    return render(request, 'checkout/checkout_success.html', context)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_intent_succeeded(payment_intent)
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_payment_intent_failed(payment_intent)

    return HttpResponse(status=200)


def handle_payment_intent_succeeded(payment_intent):
    """Handle successful payment - update booking status"""
    pid = payment_intent.id
    
    try:
        # Find booking by stripe_pid
        booking = ClassBooking.objects.get(stripe_pid=pid)
        
        # Update booking status
        booking.status = 'confirmed'
        booking.payment_status = 'paid'
        booking.save()
        
        print(f"✅ Booking {booking.booking_id} confirmed via webhook")
        
    except ClassBooking.DoesNotExist:
        print(f"❌ No booking found for payment {pid}")
    except Exception as e:
        print(f"❌ Error updating booking: {e}")


def handle_payment_intent_failed(payment_intent):
    """Handle failed payment"""
    print(f"❌ Payment failed: {payment_intent.id}")
