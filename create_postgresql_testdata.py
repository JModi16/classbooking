import os
from datetime import datetime, timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()


def main():
    from django.contrib.auth.models import User

    from profiles.models import Instructor
    from services.models import Category, ExerciseClass

    print("=== CREATING TEST DATA FOR POSTGRESQL ===\n")

    print("Creating User: Sarah Smith...")
    user, _ = User.objects.get_or_create(
        username='sarah_smith',
        defaults={
            'first_name': 'Sarah',
            'last_name': 'Smith',
            'email': 'sarah@example.com',
        },
    )
    print(f"User: {user.get_full_name()} (ID: {user.id})\n")

    print("Creating Instructor Profile...")
    instructor, created = Instructor.objects.get_or_create(
        user=user,
        defaults={
            'bio': (
                "Sarah is a certified yoga instructor with over 10 years of "
                "experience in teaching various yoga styles. Her journey began "  # noqa: E501
                "in India where she completed her 200-hour and "
                "500-hour yoga "
                "teacher training certifications.\n\n"
                "She specializes in Vinyasa and Hatha yoga, bringing a holistic "  # noqa: E501
                "approach that combines physical postures, "
                "breathing techniques, "
                "and meditation. Sarah believes in making yoga accessible to "
                "everyone, regardless of their fitness level or experience.\n\n"  # noqa: E501
                "Her classes are known for their balanced flow between challenge "  # noqa: E501
                "and relaxation, helping students build strength, "
                "flexibility, "
                "and inner peace."
            ),
            'lesson_description': (
                "Each lesson is designed to provide a complete mind-body "
                "experience. Sessions typically begin with gentle warm-ups and "  # noqa: E501
                "breathing exercises, progress through a flowing sequence of "
                "postures, and conclude with deep relaxation and "
                "meditation.\n\n"
                "What you can expect:\n"
                "- Personalized attention and modifications for all fitness "
                "levels\n"
                "- Focus on proper alignment and breathing techniques\n"
                "- A welcoming, non-judgmental environment\n"
                "- Integration of mindfulness and meditation practices\n"
                "- Progressive difficulty to help you grow at your own pace\n\n"  # noqa: E501
                "All necessary equipment (mats, blocks, straps) is provided. "
                "Please wear comfortable clothing that allows "
                "freedom of "
                "movement and bring water."
            ),
            'certifications': (
                "- 500-Hour Registered Yoga Teacher (RYT-500)\n"
                "- 200-Hour Yoga Teacher Training Certificate\n"
                "- Prenatal Yoga Certification\n"
                "- Yin Yoga Specialist\n"
                "- Meditation & Mindfulness Instructor\n"
                "- First Aid & CPR Certified"
            ),
            'years_experience': 10,
            'specialties': (
                "Vinyasa Yoga, Hatha Yoga, Yin Yoga, Prenatal Yoga, "
                "Meditation, Breathwork"
            ),
            'rating': 4.8,
            'total_reviews': 47,
            'hourly_rate': 60.00,
            'package_single_rate': 25.00,
            'package_5_rate': 110.00,
            'package_10_rate': 200.00,
            'package_monthly_rate': 150.00,
            'is_verified': True,
            'is_active': True,
            'instagram': 'https://instagram.com/sarahyoga',
        },
    )
    if created:
        print(f"Created instructor: {instructor.get_display_name()}")
    else:
        print(f"Instructor already exists: {instructor.get_display_name()}")
    print(
        "   Rating: "
            f"{instructor.rating}, Experience: "
            f"{instructor.years_experience} years\n"
    )

    print("Getting Yoga category...")
    yoga_cat, _ = Category.objects.get_or_create(
        name='Yoga',
        defaults={'friendly_name': 'Yoga'},
    )
    print(f"Category: {yoga_cat.name}\n")

    print("Creating Exercise Classes...")
    now = datetime.now()
    classes_data = [
        {
            'name': 'Morning Yoga',
            'description': (
                'Starting the day with energizing poses '
                'and breathing techniques'
            ),
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
            'description': (
                'Slow, gentle poses held for longer '
                'to relax and restore'
            ),
            'difficulty_level': 'beginner',
            'start_datetime': now + timedelta(days=3, hours=19),
            'end_datetime': now + timedelta(days=3, hours=20),
            'max_participants': 20,
            'price': 25.00,
        },
    ]

    for class_data in classes_data:
        exercise_class, class_created = ExerciseClass.objects.get_or_create(
            name=class_data['name'],
            defaults={
                'category': yoga_cat,
                'instructor': instructor,
                **class_data,
                'available': True,
            },
        )
        status = "Created" if class_created else "Already exists"
        difficulty = exercise_class.get_difficulty_level_display()
        print(
            f"{status}: {exercise_class.name} - "
            f"GBP {exercise_class.price} ({difficulty})"
        )

    print("\n=== DATA CREATION COMPLETE ===")
    print(f"Categories: {Category.objects.count()}")
    print(f"Instructors: {Instructor.objects.count()}")
    print(f"Exercise Classes: {ExerciseClass.objects.count()}")


if __name__ == '__main__':
    main()
