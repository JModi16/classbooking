from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
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
    
    # Instructor directory grouped by class type with required display counts
    from profiles.models import Instructor

    target_instructor_counts = [
        ('Personal Trainer', 3),
        ('Yoga', 3),
        ('Pilates', 2),
        ('Boxercise', 2),
    ]

    category_name_set = {name for name, _ in target_instructor_counts}
    selected_category = category if category in category_name_set else ''

    if selected_category:
        filtered_target_instructor_counts = [
            (name, count) for name, count in target_instructor_counts if name == selected_category
        ]
    else:
        filtered_target_instructor_counts = target_instructor_counts

    active_instructors = Instructor.objects.filter(
        is_active=True
    ).select_related('user').order_by('-is_verified', '-rating')

    category_instructor_sections = []
    for category_name, target_count in filtered_target_instructor_counts:
        selected_instructors = []
        selected_ids = set()

        category_obj = Category.objects.filter(name=category_name).first()

        # 1) Prioritize instructors assigned to this class type
        class_type_instructors = active_instructors.filter(
            class_type=category_name
        ).distinct()
        for instructor_item in class_type_instructors:
            if instructor_item.id not in selected_ids and len(selected_instructors) < target_count:
                selected_instructors.append(instructor_item)
                selected_ids.add(instructor_item.id)

        # 2) Next, instructors with upcoming classes in this category (if still slots available)
        if len(selected_instructors) < target_count and category_obj:
            class_instructors = active_instructors.filter(
                classes__category=category_obj,
                classes__start_datetime__gte=timezone.now(),
                classes__available=True,
            ).exclude(id__in=selected_ids).distinct()
            for instructor_item in class_instructors:
                if len(selected_instructors) < target_count:
                    selected_instructors.append(instructor_item)
                    selected_ids.add(instructor_item.id)

        # 3) Fallback: instructors whose specialties mention the category
        if len(selected_instructors) < target_count:
            specialty_instructors = active_instructors.filter(
                Q(specialties__icontains=category_name) |
                Q(specialties__icontains=category_name.replace(' ', ''))
            ).exclude(id__in=selected_ids).distinct()

            for instructor_item in specialty_instructors:
                if len(selected_instructors) < target_count:
                    selected_instructors.append(instructor_item)
                    selected_ids.add(instructor_item.id)

        # 3) Fallback to other active instructors
        if len(selected_instructors) < target_count:
            fallback_instructors = active_instructors.exclude(id__in=selected_ids)
            for instructor_item in fallback_instructors:
                if len(selected_instructors) < target_count:
                    selected_instructors.append(instructor_item)
                    selected_ids.add(instructor_item.id)

        instructor_cards = []
        for instructor_item in selected_instructors:
            brief_description = instructor_item.bio or instructor_item.lesson_description or 'Instructor profile coming soon.'
            instructor_cards.append({
                'id': instructor_item.id,
                'name': instructor_item.get_display_name(),
                'location': instructor_item.get_location(),
                'brief_description': brief_description,
            })

        # 4) Guarantee the requested number of cards even if data is incomplete
        while len(instructor_cards) < target_count:
            slot_number = len(instructor_cards) + 1
            instructor_cards.append({
                'id': None,
                'name': f'Instructor {slot_number}',
                'location': 'Location to be updated',
                'brief_description': 'Profile coming soon.',
            })

        category_instructor_sections.append({
            'category_name': category_name,
            'target_count': target_count,
            'instructors': instructor_cards,
        })

    context = {
        'classes': classes,
        'categories': categories,
        'difficulty_choices': difficulty_choices,
        'search_query': search_query,
        'category_instructor_sections': category_instructor_sections,
        'selected_category': selected_category,
        'selected_difficulty': difficulty or '',
        'selected_sort': sort or 'date',
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


def all_instructors(request):
    """Display all active instructors (each instructor once)"""
    from profiles.models import Instructor
    
    # Get all active instructors, ordered by verification and rating
    instructors = Instructor.objects.filter(
        is_active=True
    ).select_related('user').order_by('-is_verified', '-rating')
    
    context = {
        'instructors': instructors,
    }
    return render(request, 'services/instructors.html', context)
