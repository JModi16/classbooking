import os
import sys
from datetime import timedelta
import django
from django.utils import timezone
from profiles.models import Instructor
from services.models import Category, ExerciseClass
sys.path.insert(0, os.path.dirname(__file__))


django.setup()

PRIMARY = {
    'john_mcgovern': 'Personal Trainer',
    'mike_anderson': 'Personal Trainer',
    'nina_foster': 'Personal Trainer',
    'sheena_shah': 'Yoga',
    'neil_patel': 'Yoga',
    'priya_sharma': 'Yoga',
    'daniel_sullivan': 'Pilates',
    'emma_watson': 'Pilates',
    'tyler_jones': 'Boxercise',
    'james_taylor': 'Boxercise',
}

def reset_classes():
    now = timezone.now()
    all_instructors = Instructor.objects.select_related('user')
    primary_usernames = set(PRIMARY.keys())

    # 1) Keep only primary instructors active
    all_instructors.exclude(
        user__username__in=primary_usernames
    ).update(is_active=False)
    primary_instructors = all_instructors.filter(
        user__username__in=primary_usernames
    )

    # 2) Ensure primary instructor class_type + active status
    for instructor in primary_instructors:
        expected_class_type = PRIMARY[instructor.user.username]
        changed_fields = []
        if instructor.class_type != expected_class_type:
            instructor.class_type = expected_class_type
            changed_fields.append('class_type')
        if not instructor.is_active:
            instructor.is_active = True
            changed_fields.append('is_active')
        if changed_fields:
            instructor.save(update_fields=changed_fields)

    # 3) Remove ALL future classes, then recreate a clean set
    ExerciseClass.objects.filter(start_datetime__gte=now).delete()

    categories = {
        category.name: category
        for category in Category.objects.all()
    }
    if not categories:
        print('❌ No categories found. Please create categories first.')
        return

    # 4) Create exactly 2 future classes per primary instructor
    created = 0
    ordered_primary = sorted(
        primary_instructors,
        key=lambda item: item.user.username
    )

    for index, instructor in enumerate(ordered_primary):
        class_type = PRIMARY[instructor.user.username]
        category = (
            categories.get(class_type)
            or next(iter(categories.values()))
        )
        price = (
            instructor.package_single_rate
            or instructor.hourly_rate
            or 20.00
        )
        display_name = instructor.get_display_name()

        for slot in range(2):
            day_offset = (index * 2) + slot + 1
            start_hour = 10 if slot == 0 else 18
            start_datetime = (now + timedelta(days=day_offset)).replace(
                hour=start_hour,
                minute=0,
                second=0,
                microsecond=0,
            )
            end_datetime = start_datetime + timedelta(hours=1)

            ExerciseClass.objects.create(
                name=(
                    f'{class_type} - {display_name} (Session {slot + 1})'
                ),
                description=(
                    f'{class_type} training session with {display_name}.'
                ),
                category=category,
                instructor=instructor,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                max_participants=15,
                price=price,
                difficulty_level='intermediate',
                available=True,
            )
            created += 1

    print('✅ Reset complete')
    print(f'Primary instructors: {primary_instructors.count()}/10')
    print(f'Upcoming classes created: {created} (expected 20)')


if __name__ == '__main__':
    reset_classes()
