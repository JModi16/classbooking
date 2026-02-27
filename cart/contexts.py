from decimal import Decimal
from django.conf import settings


def cart_contents(request):
    """
    Context processor for cart contents
    """
    cart_items = []
    total = 0
    service_count = 0
    cart = request.session.get('cart', {})

    context = {
        'cart_items': cart_items,
        'total': total,
        'service_count': service_count,
    }

    return context
