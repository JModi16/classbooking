from django.contrib import messages
from django.shortcuts import redirect, render

from services.models import Category


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
            messages.success(request, 'Thanks for your message. We will contact you shortly.')
            return redirect('contact')

        messages.error(request, 'Please complete all fields before sending your message.')

    context = {
        'categories': categories,
        'form_data': form_data,
    }
    return render(request, 'home/contact.html', context)
