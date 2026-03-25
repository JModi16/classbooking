from decimal import Decimal
from django.conf import settings
from .utils import build_cart_items


def cart_contents(request):
    """
    Context processor for class booking cart contents
    """
    cart = request.session.get("cart", {})
    cart_items, total, class_count = build_cart_items(cart)

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        "cart_items": cart_items,
        "total": total,
        "class_count": class_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }

    return context
