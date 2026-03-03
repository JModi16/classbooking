import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()

from profiles.models import Instructor
from services.models import ExerciseClass

print('=== INSTRUCTORS ===')
instructors = Instructor.objects.all()
for i in instructors:
    print(f'{i.get_display_name()}')
    print(f'  Bio: {i.bio[:80] if i.bio else "No bio"}...')
    print(f'  Specialties: {i.specialties}')
    print(f'  Image: {bool(i.image)}')
    print(f'  Rating: {i.rating}')
    print()

print('\n=== CLASSES ===')
classes = ExerciseClass.objects.all()[:5]
for c in classes:
    print(f'{c.name} - £{c.price} - Instructor: {c.instructor.get_display_name()}')
