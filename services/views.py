from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Service, Category, ExerciseClass


def all_services(request):
    """Display all services with filtering and sorting (legacy)"""
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
    """Display service details (legacy)"""
    service = Service.objects.get(id=service_id)
    context = {
        'service': service,
    }
    return render(request, 'services/service_detail.html', context)


# Exercise Class Views
def all_classes(request):
    """Display all upcoming exercise classes with filtering and sorting"""
    # Only show future classes
    classes = ExerciseClass.objects.filter(
        start_datetime__gte=timezone.now(),
        available=True
    ).select_related('instructor', 'category')
    
    categories = Category.objects.all()
    search_query = None
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        search_query = search
        classes = classes.filter(
            name__icontains=search
        ) | classes.filter(
            description__icontains=search
        ) | classes.filter(
            instructor__user__first_name__icontains=search
        ) | classes.filter(
            instructor__user__last_name__icontains=search
        )
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        classes = classes.filter(category__name=category)
    
    # Filter by difficulty level
    difficulty = request.GET.get('difficulty')
    if difficulty:
        classes = classes.filter(difficulty_level=difficulty)
    
    # Filter by instructor
    instructor = request.GET.get('instructor')
    if instructor:
        classes = classes.filter(instructor__id=instructor)
    
    # Sorting
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        classes = classes.order_by('price')
    elif sort == 'price_desc':
        classes = classes.order_by('-price')
    elif sort == 'rating':
        classes = classes.order_by('-instructor__rating')
    elif sort == 'date':
        classes = classes.order_by('start_datetime')
    else:
        # Default: sort by start time
        classes = classes.order_by('start_datetime')
    
    difficulty_choices = ExerciseClass.DIFFICULTY_CHOICES
    
    context = {
        'classes': classes,
        'categories': categories,
        'difficulty_choices': difficulty_choices,
        'search_query': search_query,
    }
    return render(request, 'services/classes.html', context)


def class_detail(request, class_id):
    """Display exercise class details and booking option"""
    exercise_class = get_object_or_404(ExerciseClass, id=class_id)
    available_spots = exercise_class.get_available_spots()
    is_full = exercise_class.is_full()
    is_upcoming = exercise_class.is_upcoming()
    
    # Get instructor profile
    instructor = exercise_class.instructor
    
    context = {
        'exercise_class': exercise_class,
        'instructor': instructor,
        'available_spots': available_spots,
        'is_full': is_full,
        'is_upcoming': is_upcoming,
    }
    return render(request, 'services/class_detail.html', context)


def instructor_profile(request, instructor_id):
    """Display instructor profile and their classes"""
    from profiles.models import Instructor
    
    instructor = get_object_or_404(Instructor, id=instructor_id)
    
    # Get instructor's upcoming classes
    classes = ExerciseClass.objects.filter(
        instructor=instructor,
        start_datetime__gte=timezone.now(),
        available=True
    ).order_by('start_datetime')
    
    context = {
        'instructor': instructor,
        'classes': classes,
    }
    return render(request, 'services/instructor_profile.html', context)
