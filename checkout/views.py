from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
import stripe
import json
import uuid
import logging
from allauth.account.models import EmailAddress
from .models import ClassBooking, ClassBookingLineItem
from cart.utils import build_cart_items

logger = logging.getLogger(__name__)


def get_booking_recipient_email(booking):
    """Get recipient email, prioritizing allauth primary verified address."""
    primary_verified = EmailAddress.objects.filter(
        user=booking.user,
        verified=True,
        primary=True,
    ).first()
    if primary_verified:
        return primary_verified.email

    verified_email = EmailAddress.objects.filter(user=booking.user, verified=True).first()
    if verified_email:
        return verified_email.email

    if booking.email:
        return booking.email

    return booking.user.email


def send_booking_confirmation_email(booking):
    """Send booking confirmation email once."""
    if booking.confirmation_email_sent:
        return

    if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
        logger.warning('EMAIL_BACKEND is console; confirmation email is printed to terminal and not delivered to inbox.')

    recipient = get_booking_recipient_email(booking)
    if not recipient:
        logger.warning(f'No recipient email available for booking {booking.booking_id}')
        return

    context = {
        'booking': booking,
        'line_items': booking.line_items.all(),
        'support_email': settings.SUPPORT_EMAIL,
    }

    subject = f'Booking Confirmation - {booking.booking_id}'
    text_body = render_to_string('emails/booking_confirmation.txt', context)
    html_body = render_to_string('emails/booking_confirmation.html', context)

    try:
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )
        email_message.attach_alternative(html_body, 'text/html')
        email_message.send()

        booking.confirmation_email_sent = True
        booking.confirmation_email_sent_at = timezone.now()
        booking.save(update_fields=['confirmation_email_sent', 'confirmation_email_sent_at', 'updated_at'])
        logger.info(f'Booking confirmation email sent for {booking.booking_id} to {recipient}')
    except Exception as exc:
        logger.error(f'Failed to send booking confirmation email for {booking.booking_id}: {exc}')


@login_required
@require_http_methods(["GET", "POST"])
def checkout(request):
    """Checkout page for class bookings"""
    # Set Stripe API key at request time
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
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

            send_booking_confirmation_email(booking)

            # Clear cart
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True
            return redirect('checkout_success', booking_id=booking.booking_id)
        except ClassBooking.DoesNotExist:
            messages.error(request, 'Booking not found. Please contact support.')
            return redirect('view_cart')
    
    # GET request - Build cart items (classes + packages)
    cart_items, total, _ = build_cart_items(cart)
    
    if not cart_items:
        messages.error(request, 'No valid items in cart')
        return redirect('view_cart')
    
    # Apply delivery threshold logic if applicable (set to 0 for class bookings)
    delivery = 0
    grand_total = total + delivery
    
    # Create Stripe Payment Intent
    stripe_total = round(float(grand_total) * 100)  # Stripe expects amount in pence
    
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
    # Set Stripe API key at request time
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    try:
        # Get client_secret from POST data
        logger.debug(f'POST data: {request.POST}')
        logger.debug(f'Body: {request.body}')
        client_secret = request.POST.get('client_secret')
        if not client_secret:
            # Try JSON body for backwards compatibility
            try:
                data = json.loads(request.body)
                client_secret = data.get('client_secret')
                logger.debug(f'Got client_secret from JSON: {client_secret}')
            except Exception as e:
                logger.debug(f'Failed to parse JSON: {e}')
        
        if not client_secret:
            logger.error('Missing client secret in cache_checkout_data')
            return JsonResponse({'error': 'Missing client secret'}, status=400)
            
        pid = client_secret.split('_secret')[0]
        cart = request.session.get('cart', {})

        # Get cart items and create booking
        cart_items, total, _ = build_cart_items(cart)

        if not cart_items:
            return JsonResponse({'error': 'No valid items in cart'}, status=400)

        first_class_item = next((item for item in cart_items if item['item_type'] == 'class'), None)
        course = first_class_item['exercise_class'] if first_class_item else None

        # For package-only carts, capture the instructor from the first package item
        first_package_item = next((item for item in cart_items if item['item_type'] == 'package'), None)
        booking_instructor = None
        if course:
            booking_instructor = course.instructor
        elif first_package_item:
            booking_instructor = first_package_item['instructor']

        # Create booking with pending status
        booking = ClassBooking.objects.create(
            booking_id=uuid.uuid4().hex,
            user=request.user,
            course=course,
            instructor=booking_instructor,
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
                item_type='class' if item['item_type'] == 'class' else 'addon',
                description=item['display_name'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
            )
        
        # Update Payment Intent metadata
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(cart),
            'username': request.user.username,
            'user_id': request.user.id,
            'booking_id': str(booking.booking_id),
        })
        
        logger.debug(f'Booking created successfully: {booking.booking_id}')
        return JsonResponse({'success': True, 'booking_id': str(booking.booking_id)})
    except Exception as e:
        logger.error(f'Error in cache_checkout_data: {type(e).__name__}: {str(e)}', exc_info=True)
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
    wh_secret = settings.STRIPE_WH_SECRET

    if not wh_secret:
        logger.error('STRIPE_WH_SECRET is not configured')
        return HttpResponse('Webhook secret not configured', status=500)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        logger.warning(f'Stripe webhook invalid payload: {e}')
        return HttpResponse(status=400)
    except (stripe.error.SignatureVerificationError, stripe.SignatureVerificationError) as e:
        logger.warning(f'Stripe webhook invalid signature: {e}')
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f'Stripe webhook construct_event failed: {type(e).__name__}: {e}')
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
        booking = ClassBooking.objects.get(stripe_pid=pid)
        booking.status = 'confirmed'
        booking.payment_status = 'paid'
        booking.save()
        send_booking_confirmation_email(booking)
        logger.info(f'Booking {booking.booking_id} confirmed via webhook')
    except ClassBooking.DoesNotExist:
        logger.warning(f'No booking found for payment intent {pid}')
    except Exception as e:
        logger.error(f'Error updating booking for payment intent {pid}: {type(e).__name__}: {e}', exc_info=True)


def handle_payment_intent_failed(payment_intent):
    """Handle failed payment"""
    print(f"❌ Payment failed: {payment_intent.id}")
