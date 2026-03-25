from django.core.management.base import BaseCommand, CommandError

from checkout.models import ClassBooking
from checkout.views import send_booking_confirmation_email


class Command(BaseCommand):
    help = "Send booking confirmation email for a booking ID."

    def add_arguments(self, parser):
        parser.add_argument(
            "booking_id", type=str, help="Booking ID to send email for"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help=(
                "Resend even if confirmation email was already "
                "marked as sent"
            ),
        )

    def handle(self, *args, **options):
        booking_id = options["booking_id"]
        force = options["force"]

        try:
            booking = ClassBooking.objects.get(booking_id=booking_id)
        except ClassBooking.DoesNotExist as exc:
            raise CommandError(
                f"Booking with ID '{booking_id}' does not exist."
            ) from exc

        already_sent = booking.confirmation_email_sent
        if already_sent and force:
            booking.confirmation_email_sent = False
            booking.confirmation_email_sent_at = None
            booking.save(
                update_fields=[
                    "confirmation_email_sent",
                    "confirmation_email_sent_at",
                    "updated_at",
                ]
            )

        send_booking_confirmation_email(booking)
        booking.refresh_from_db(
            fields=["confirmation_email_sent", "confirmation_email_sent_at"]
        )

        if booking.confirmation_email_sent:
            if already_sent and not force:
                self.stdout.write(
                    self.style.WARNING(
                        f"Email already marked as sent for booking "
                        f"{booking.booking_id}."
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Email send attempt completed for booking "
                        f"{booking.booking_id}."
                    )
                )
            self.stdout.write(
                "Recipient email on booking record: "
                f"{booking.email or '(none)'}"
            )
            return

        raise CommandError(
            "Email send did not complete successfully. Check logs "
            "and SMTP settings (EMAIL_HOST_USER/PASSWORD)."
        )
