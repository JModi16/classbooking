from decimal import Decimal
from django.conf import settings


def cart_contents(request):
    """
    Context processor for class booking cart contents
    """
    cart_items = []
    total = 0
    class_count = 0
    cart = request.session.get('cart', {})

    # Process cart items (class bookings)
    for class_id, quantity in cart.items():
        try:
            from services.models import ExerciseClass
            exercise_class = ExerciseClass.objects.get(id=class_id)
            
            # Check availability
            available_spots = exercise_class.get_available_spots()
            
            # Quantity represents number of participants booking
            if quantity > available_spots:
                quantity = available_spots
            
            item_total = Decimal(exercise_class.price) * quantity
            total += item_total
            class_count += quantity
            
            cart_items.append({
                'class_id': class_id,
                'class': exercise_class,
                'quantity': quantity,
                'item_total': item_total,
                'available_spots': available_spots,
            })
        except ExerciseClass.DoesNotExist:
            continue

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'class_count': class_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
