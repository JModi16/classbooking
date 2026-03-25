from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Send a direct test email to any address to "
        "validate SMTP configuration."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "to_email", type=str, help="Recipient email address"
        )
        parser.add_argument(
            "--subject",
            type=str,
            default="Service Booking Platform test email",
            help="Optional subject line",
        )

    def handle(self, *args, **options):
        to_email = options["to_email"]
        subject = options["subject"]
        from_email = settings.DEFAULT_FROM_EMAIL

        if (
            settings.EMAIL_BACKEND
            == "django.core.mail.backends.console.EmailBackend"
        ):
            raise CommandError(
                "EMAIL_BACKEND is set to console, so messages are "
                "only printed in terminal. Set EMAIL_BACKEND to "
                "django.core.mail.backends.smtp.EmailBackend and configure "
                "EMAIL_HOST_USER/EMAIL_HOST_PASSWORD."
            )

        text_body = (
            "This is a direct SMTP test email from "
            "Service Booking Platform.\n\n"
            "If you received this message, your outbound email "
            "configuration is working."
        )
        html_body = (
            "<p>This is a direct SMTP test email from "
            "<strong>Service Booking Platform</strong>.</p>"
            "<p>If you received this message, your outbound "
            "email configuration is working.</p>"
        )

        try:
            message = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=from_email,
                to=[to_email],
            )
            message.attach_alternative(html_body, "text/html")
            message.send()
        except Exception as exc:
            raise CommandError(f"Failed to send test email: {exc}") from exc

        self.stdout.write(
            self.style.SUCCESS(f"Test email sent to {to_email}.")
        )
        self.stdout.write(f"From: {from_email}")
        self.stdout.write(f"Backend: {settings.EMAIL_BACKEND}")
