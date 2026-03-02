from django.contrib import admin
from .models import Order, OrderLineItem, ClassBooking, ClassBookingLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'order_total', 'grand_total', 'original_cart', 'stripe_pid')
    list_display = ('order_number', 'date', 'full_name', 'grand_total')
    list_filter = ('date', 'user_profile')


class ClassBookingLineItemAdminInline(admin.TabularInline):
    model = ClassBookingLineItem
    readonly_fields = ('line_total',)
    extra = 0


class ClassBookingAdmin(admin.ModelAdmin):
    inlines = (ClassBookingLineItemAdminInline,)
    readonly_fields = ('booking_id', 'created_at', 'updated_at', 'booking_date')
    
    fieldsets = (
        ('Booking Info', {
            'fields': ('booking_id', 'user', 'course')
        }),
        ('Participant Details', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Status & Payment', {
            'fields': ('status', 'payment_status', 'total_amount', 'stripe_pid')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('created_at', 'updated_at', 'booking_date'),
            'classes': ('collapse',)
        }),
    )
    
    list_display = ('booking_id', 'user', 'course', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at', 'course__category')
    search_fields = ('booking_id', 'user__username', 'user__email', 'full_name', 'email')
    date_hierarchy = 'created_at'


admin.site.register(Order, OrderAdmin)
admin.site.register(ClassBooking, ClassBookingAdmin)
