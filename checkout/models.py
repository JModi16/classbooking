from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from services.models import Service, ExerciseClass
import uuid


# Booking statuses
BOOKING_STATUS_CHOICES = [
    ('pending', 'Pending Payment'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
]

PAYMENT_STATUS_CHOICES = [
    ('unpaid', 'Unpaid'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
]


class Order(models.Model):
    """Legacy order model for backward compatibility"""
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey('profiles.UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """Legacy order line item model"""
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    service = models.ForeignKey(Service, null=False, blank=False, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = self.service.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.service.sku} on order {self.order.order_number}'


class ClassBooking(models.Model):
    """Booking for exercise classes by users with personal instructors"""
    booking_id = models.CharField(max_length=32, null=False, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_bookings')
    user_profile = models.ForeignKey('profiles.UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Booking details
    course = models.ForeignKey(ExerciseClass, on_delete=models.PROTECT, related_name='bookings', null=True, blank=True)
    
    # Participant info
    full_name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    
    # Pricing
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment reference
    stripe_pid = models.CharField(max_length=254, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['stripe_pid']),
        ]

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username}"

    def get_instructor(self):
        """Get the instructor for this booking"""
        if not self.course:
            return None
        return self.course.instructor

    def get_class_date(self):
        """Get the class date"""
        if not self.course:
            return None
        return self.course.start_datetime.date()


class ClassBookingLineItem(models.Model):
    """Individual line item for a class booking (can have add-ons)"""
    booking = models.ForeignKey(ClassBooking, on_delete=models.CASCADE, related_name='line_items')
    
    # Item type (class or add-on)
    ITEM_TYPE_CHOICES = [
        ('class', 'Exercise Class'),
        ('addon', 'Add-on (e.g., equipment rental)'),
    ]
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default='class')
    
    # Description
    description = models.CharField(max_length=254, help_text="e.g., Class name or add-on name")
    
    # Quantity & Pricing
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} x{self.quantity} - {self.booking.booking_id}"
