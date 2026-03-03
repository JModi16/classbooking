import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()

from django.contrib.auth.models import User
from datetime import datetime, timedelta
from profiles.models import Instructor
from services.models import Category, ExerciseClass

print("=== CREATING TEST DATA FOR POSTGRESQL ===\n")

# 1. Create Sarah Smith user if not exists
print("Creating User: Sarah Smith...")
user, created = User.objects.get_or_create(
    username='sarah_smith',
    defaults={
        'first_name': 'Sarah',
        'last_name': 'Smith',
        'email': 'sarah@example.com'
    }
)
print(f"✅ User: {user.get_full_name()} (ID: {user.id})\n")

# 2. Create Instructor profile
print("Creating Instructor Profile...")
instructor, created = Instructor.objects.get_or_create(
    user=user,
    defaults={
        'bio': """Sarah is a certified yoga instructor with over 10 years of experience in teaching various yoga styles. Her journey began in India where she completed her 200-hour and 500-hour yoga teacher training certifications.

She specializes in Vinyasa and Hatha yoga, bringing a holistic approach that combines physical postures, breathing techniques, and meditation. Sarah believes in making yoga accessible to everyone, regardless of their fitness level or experience.

Her classes are known for their balanced flow between challenge and relaxation, helping students build strength, flexibility, and inner peace.""",
        'lesson_description': """Each lesson is designed to provide a complete mind-body experience. Sessions typically begin with gentle warm-ups and breathing exercises, progress through a flowing sequence of postures, and conclude with deep relaxation and meditation.

What you can expect:
• Personalized attention and modifications for all fitness levels
• Focus on proper alignment and breathing techniques
• A welcoming, non-judgmental environment
• Integration of mindfulness and meditation practices
• Progressive difficulty to help you grow at your own pace

All necessary equipment (mats, blocks, straps) is provided. Please wear comfortable clothing that allows freedom of movement and bring water.""",
        'certifications': """- 500-Hour Registered Yoga Teacher (RYT-500)
- 200-Hour Yoga Teacher Training Certificate
- Prenatal Yoga Certification
- Yin Yoga Specialist
- Meditation & Mindfulness Instructor
- First Aid & CPR Certified""",
        'years_experience': 10,
        'specialties': "Vinyasa Yoga, Hatha Yoga, Yin Yoga, Prenatal Yoga, Meditation, Breathwork",
        'rating': 4.8,
        'total_reviews': 47,
        'hourly_rate': 60.00,
        'package_single_rate': 25.00,
        'package_5_rate': 110.00,
        'package_10_rate': 200.00,
        'package_monthly_rate': 150.00,
        'is_verified': True,
        'is_active': True,
        'instagram': 'https://instagram.com/sarahyoga'
    }
)
if created:
    print(f"✅ Created Instructor: {instructor.get_display_name()}")
else:
    print(f"✅ Instructor already exists: {instructor.get_display_name()}")
print(f"   Rating: {instructor.rating}, Experience: {instructor.years_experience} years\n")

# 3. Get or create Yoga category
print("Getting Yoga category...")
yoga_cat, _ = Category.objects.get_or_create(
    name='Yoga',
    defaults={'friendly_name': 'Yoga'}
)
print(f"✅ Category: {yoga_cat.name}\n")

# 4. Create test classes
print("Creating Exercise Classes...")
now = datetime.now()
classes_data = [
    {
        'name': 'Morning Yoga',
        'description': 'Starting the day with energizing poses and breathing techniques',
        'difficulty_level': 'beginner',
        'start_datetime': now + timedelta(days=1, hours=7),
        'end_datetime': now + timedelta(days=1, hours=8),
        'max_participants': 20,
        'price': 25.00,
    },
    {
        'name': 'Evening Yoga Flow',
        'description': 'Relaxing vinyasa flow to unwind after the day',
        'difficulty_level': 'intermediate',
        'start_datetime': now + timedelta(days=1, hours=18),
        'end_datetime': now + timedelta(days=1, hours=19),
        'max_participants': 20,
        'price': 25.00,
    },
    {
        'name': 'Advanced Vinyasa',
        'description': 'Fast-paced vinyasa flow for experienced yogis',
        'difficulty_level': 'advanced',
        'start_datetime': now + timedelta(days=2, hours=9),
        'end_datetime': now + timedelta(days=2, hours=10),
        'max_participants': 15,
        'price': 30.00,
    },
    {
        'name': 'Restorative Yoga',
        'description': 'Slow, gentle poses held for longer to relax and restore',
        'difficulty_level': 'beginner',
        'start_datetime': now + timedelta(days=3, hours=19),
        'end_datetime': now + timedelta(days=3, hours=20),
        'max_participants': 20,
        'price': 25.00,
    },
]

for class_data in classes_data:
    exercise_class, created = ExerciseClass.objects.get_or_create(
        name=class_data['name'],
        defaults={
            'category': yoga_cat,
            'instructor': instructor,
            **class_data,
            'available': True,
        }
    )
    status = "✅ Created" if created else "⚠️  Already exists"
    print(f"{status}: {exercise_class.name} - £{exercise_class.price} ({exercise_class.get_difficulty_level_display()})")

print("\n=== DATA CREATION COMPLETE ===")
print(f"✅ Categories: {Category.objects.count()}")
print(f"✅ Instructors: {Instructor.objects.count()}")
print(f"✅ Exercise Classes: {ExerciseClass.objects.count()}")
