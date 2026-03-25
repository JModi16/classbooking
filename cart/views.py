from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from services.models import ExerciseClass
from profiles.models import Instructor
from .utils import build_cart_items, build_package_key, get_package_option


def view_cart(request):
    """Display shopping cart with bookings"""
    cart = request.session.get("cart", {})
    cart_items, total, _ = build_cart_items(cart)

    if total < getattr(settings, "FREE_DELIVERY_THRESHOLD", 0):
        delivery = (
            total * getattr(settings, "STANDARD_DELIVERY_PERCENTAGE", 0) / 100
        )
    else:
        delivery = 0

    grand_total = total + delivery

    context = {
        "cart_items": cart_items,
        "total": total,
        "delivery": delivery,
        "grand_total": grand_total,
    }
    return render(request, "cart/cart.html", context)


@login_required
def add_class_to_cart(request, class_id):
    """Add exercise class booking to cart"""
    exercise_class = get_object_or_404(ExerciseClass, id=class_id)

    # Check if class is available
    if exercise_class.is_full():
        return JsonResponse({"success": False, "message": "Class is full"})

    if not exercise_class.is_upcoming():
        return JsonResponse(
            {"success": False, "message": "This class has already passed"}
        )

    cart = request.session.get("cart", {})
    class_id_str = str(class_id)

    # For class bookings, quantity is typically 1 (booking for yourself)
    # but could be multiple if helping someone else book
    quantity = request.POST.get("quantity", 1)
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        quantity = 1

    # Check if we have enough spots
    available = exercise_class.get_available_spots()
    if quantity > available:
        return JsonResponse(
            {
                "success": False,
                "message": f"Only {available} spot(s) available",
            }
        )

    if class_id_str in cart:
        cart[class_id_str] += quantity
    else:
        cart[class_id_str] = quantity

    request.session["cart"] = cart
    return JsonResponse(
        {
            "success": True,
            "cart_count": sum(cart.values()),
            "message": f"Added {quantity} spot(s) to booking",
        }
    )


@login_required
def add_package_to_cart(request, instructor_id, package_type):
    """Add instructor package option to cart"""
    instructor = get_object_or_404(
        Instructor, id=instructor_id, is_active=True
    )
    package_option = get_package_option(instructor, package_type)

    if not package_option:
        return JsonResponse(
            {
                "success": False,
                "message": "This package option is not available",
            }
        )

    cart = request.session.get("cart", {})
    package_key = build_package_key(instructor_id, package_type)

    quantity = request.POST.get("quantity", 1)
    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, quantity)

    if package_key in cart:
        cart[package_key] += quantity
    else:
        cart[package_key] = quantity

    request.session["cart"] = cart
    return JsonResponse(
        {
            "success": True,
            "cart_count": sum(cart.values()),
            "message": f"Added {package_option['label']} to booking",
        }
    )


def remove_from_cart(request, class_id):
    """Remove class booking from cart"""
    cart = request.session.get("cart", {})
    class_id_str = str(class_id)

    if class_id_str in cart:
        del cart[class_id_str]

    request.session["cart"] = cart
    return JsonResponse({"success": True})


@login_required
def remove_package_from_cart(request, instructor_id, package_type):
    """Remove package booking from cart"""
    cart = request.session.get("cart", {})
    package_key = build_package_key(instructor_id, package_type)

    if package_key in cart:
        del cart[package_key]

    request.session["cart"] = cart
    return JsonResponse({"success": True})


def update_quantity(request, class_id):
    """Update quantity of class booking in cart"""
    cart = request.session.get("cart", {})
    class_id_str = str(class_id)

    if class_id_str not in cart:
        return JsonResponse({"success": False, "message": "Item not in cart"})

    try:
        exercise_class = ExerciseClass.objects.get(id=class_id)
        quantity = int(request.POST.get("quantity", 1))

        # Validate quantity doesn't exceed available spots
        available = exercise_class.get_available_spots()
        if quantity > available:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Only {available} spot(s) available",
                }
            )

        if quantity <= 0:
            if class_id_str in cart:
                del cart[class_id_str]
        else:
            cart[class_id_str] = quantity

        request.session["cart"] = cart
        return JsonResponse({"success": True})
    except ExerciseClass.DoesNotExist:
        return JsonResponse({"success": False, "message": "Class not found"})


# Legacy cart views for products (kept for backward compatibility)
def add_to_cart(request, service_id):
    """Add service to cart (legacy)"""
    cart = request.session.get("cart", {})
    service_id = str(service_id)

    if service_id in cart:
        cart[service_id] += 1
    else:
        cart[service_id] = 1

    request.session["cart"] = cart
    return JsonResponse({"success": True, "cart_count": sum(cart.values())})
