from django.shortcuts import render
from .models import Service, Category


def all_services(request):
    """Display all services with filtering and sorting"""
    services = Service.objects.all()
    categories = Category.objects.all()
    
    category = request.GET.get('category')
    if category:
        services = services.filter(category__name=category)
    
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        services = services.order_by('price')
    elif sort == 'price_desc':
        services = services.order_by('-price')
    elif sort == 'rating':
        services = services.order_by('-rating')
    
    context = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'services/services.html', context)


def service_detail(request, service_id):
    """Display service details"""
    service = Service.objects.get(id=service_id)
    context = {
        'service': service,
    }
    return render(request, 'services/service_detail.html', context)
