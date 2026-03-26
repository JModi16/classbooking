from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from checkout.models import ClassBooking

BOOKING_LOCATION_ADDRESS = (
    "Stanmore Place Fitness Studio, Howard Road, Edgware, HA8 1FA"
)


@login_required
def my_bookings(request):
    """Display user's class bookings"""
    bookings = (
        ClassBooking.objects.filter(user=request.user)
        .select_related("course", "course__instructor", "instructor")
        .prefetch_related("line_items")
        .order_by("-created_at")
    )

    # Separate into upcoming and past bookings
    now = timezone.now()
    upcoming_bookings = bookings.filter(
        Q(course__start_datetime__gte=now) | Q(course__isnull=True)
    )
    past_bookings = bookings.filter(course__start_datetime__lt=now)

    context = {
        "bookings": bookings,
        "upcoming_bookings": upcoming_bookings,
        "past_bookings": past_bookings,
        "booking_location_address": BOOKING_LOCATION_ADDRESS,
    }
    return render(request, "bookings/my_bookings.html", context)


@login_required
def booking_detail(request, booking_id):
    """Display booking details"""
    booking = get_object_or_404(
        ClassBooking, booking_id=booking_id, user=request.user
    )

    context = {
        "booking": booking,
        "now": timezone.now(),
        "booking_location_address": BOOKING_LOCATION_ADDRESS,
    }
    return render(request, "bookings/booking_detail.html", context)


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(
        ClassBooking, booking_id=booking_id, user=request.user
    )

    if not booking.course:
        messages.error(
            request, "This booking does not have a scheduled class to cancel."
        )
        return redirect("booking_detail", booking_id=booking_id)

    if not booking.can_cancel():
        messages.error(
            request,
            "Classes can only be cancelled more than 24 hours "
            "before the scheduled start time.",
        )
        return redirect("booking_detail", booking_id=booking_id)

    if request.method == "POST":
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Your booking has been cancelled.")
        return redirect("my_bookings")

    context = {
        "booking": booking,
    }
    return render(request, "bookings/cancel_booking.html", context)
