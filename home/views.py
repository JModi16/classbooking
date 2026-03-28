from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
import logging

from services.models import Category


logger = logging.getLogger(__name__)


def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')


def contact(request):
    """A view to return the contact page"""
    categories = Category.objects.all().order_by('friendly_name', 'name')
    form_data = {
        'name': '',
        'phone': '',
        'email': '',
        'class_type': '',
        'message': '',
    }

    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'class_type': request.POST.get('class_type', '').strip(),
            'message': request.POST.get('message', '').strip(),
        }

        if all(form_data.values()):
            subject = f"New Contact Form Message - {form_data['class_type']}"
            message = (
                "A new message was submitted from the contact form.\n\n"
                f"Name: {form_data['name']}\n"
                f"Phone: {form_data['phone']}\n"
                f"Email: {form_data['email']}\n"
                f"Class Type: {form_data['class_type']}\n\n"
                "Message:\n"
                f"{form_data['message']}\n"
            )

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    'Thanks for your message. We will contact you shortly.',
                )
                return redirect('contact')
            except Exception as exc:
                logger.error(f"Contact form email failed: {exc}")
                messages.error(
                    request,
                    'Sorry, your message could not be sent right now. '
                    'Please try again shortly.',
                )
                context = {
                    'categories': categories,
                    'form_data': form_data,
                }
                return render(request, 'home/contact.html', context)

        messages.error(request, 'Please complete all fields before sending your message.')

    context = {
        'categories': categories,
        'form_data': form_data,
    }
    return render(request, 'home/contact.html', context)
