from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from checkout.models import ClassBooking


@login_required
def my_bookings(request):
    """Display user's class bookings"""
    bookings = ClassBooking.objects.filter(user=request.user).select_related('course', 'course__instructor').prefetch_related('line_items').order_by('-created_at')
    
    # Separate into upcoming and past bookings
    now = timezone.now()
    upcoming_bookings = bookings.filter(Q(course__start_datetime__gte=now) | Q(course__isnull=True))
    past_bookings = bookings.filter(course__start_datetime__lt=now)
    
    context = {
        'bookings': bookings,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
    }
    return render(request, 'bookings/my_bookings.html', context)


@login_required
def booking_detail(request, booking_id):
    """Display booking details"""
    booking = get_object_or_404(ClassBooking, booking_id=booking_id, user=request.user)
    
    context = {
        'booking': booking,
        'now': timezone.now(),
    }
    return render(request, 'bookings/booking_detail.html', context)


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(ClassBooking, booking_id=booking_id, user=request.user)

    if not booking.course:
        messages.error(request, 'This booking does not have a scheduled class to cancel.')
        return redirect('booking_detail', booking_id=booking_id)
    
    # Check if class hasn't started yet
    if booking.course and booking.course.start_datetime <= timezone.now():
        messages.error(request, 'Cannot cancel a booking for a class that has already started.')
        return redirect('booking_detail', booking_id=booking_id)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
        return redirect('my_bookings')
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/cancel_booking.html', context)
