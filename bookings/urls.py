from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_bookings, name="my_bookings"),
    path("<str:booking_id>/", views.booking_detail, name="booking_detail"),
    path(
        "<str:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"
    ),
]
