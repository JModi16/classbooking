from django.core.files.base import ContentFile
from profiles.models import Instructor, UserProfile
from django.contrib.auth.models import User
import os
import sys
import django
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()


# 10 instructors with exclusive class type assignments
INSTRUCTORS = [
    # Personal Trainer (3)
    {
        'username': 'john_mcgovern',
        'first_name': 'John',
        'last_name': 'McGovern',
        'email': 'john.mcgovern@classbooking.com',
        'class_type': 'Personal Trainer',
        'specialties': 'Strength Training, HIIT, Weight Loss, Functional Fitness',  # noqa: E501
        'bio': 'John is a certified personal trainer with 6 years of experience specializing in strength training and HIIT workouts. He has helped clients achieve dramatic transformations through personalized training programs.',  # noqa: E501
        'lesson_description': 'Customized personal training sessions focused on your specific goals. Each session includes warm-up, targeted strength/cardio work, and proper cool-down. Perfect for weight loss, muscle building, or overall fitness improvement.',  # noqa: E501
        'certifications': 'NASM Certified Personal Trainer, CPR/AED, Nutrition Specialist',  # noqa: E501
        'years_experience': 6,
        'hourly_rate': 55.00,
        'package_single_rate': 25.00,
        'package_5_rate': 110.00,
        'package_10_rate': 200.00,
        'package_monthly_rate': 180.00,
        'rating': 4.9,
        'total_reviews': 89,
        'location': {'city': 'London', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/john_fitness',
        'is_verified': True,
        'color': (255, 140, 0),  # Orange
    },
    {
        'username': 'mike_anderson',
        'first_name': 'Mike',
        'last_name': 'Anderson',
        'email': 'mike.anderson@classbooking.com',
        'class_type': 'Personal Trainer',
        'specialties': 'Boxing Training, Fitness Boxing, Athletic Performance',
        'bio': 'Mike is a professional boxing coach with 10 years of competitive and coaching experience. He specializes in athletic performance training that combines boxing techniques with strength and conditioning.',  # noqa: E501
        'lesson_description': 'High-performance training that blends boxing skills with strength and conditioning. Sessions emphasize explosive power, speed development, and functional fitness through boxing-based workouts.',  # noqa: E501
        'certifications': 'Professional Boxing Coach, ISSA Elite Trainer, Sports Performance Specialist',  # noqa: E501
        'years_experience': 10,
        'hourly_rate': 60.00,
        'package_single_rate': 28.00,
        'package_5_rate': 125.00,
        'package_10_rate': 220.00,
        'package_monthly_rate': 200.00,
        'rating': 4.8,
        'total_reviews': 102,
        'location': {'city': 'Liverpool', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/mike_performance',
        'is_verified': True,
        'color': (220, 100, 40),  # Dark Orange
    },
    {
        'username': 'nina_foster',
        'first_name': 'Nina',
        'last_name': 'Foster',
        'email': 'nina.foster@classbooking.com',
        'class_type': 'Personal Trainer',
        'specialties': 'Weight Management, Metabolic Training, Body Transformation',  # noqa: E501
        'bio': 'Nina is a transformation specialist with 5 years of experience helping clients achieve sustainable weight loss and body composition changes through evidence-based training and lifestyle coaching.',  # noqa: E501
        'lesson_description': 'Results-driven personal training focused on fat loss and metabolic health. Combines resistance training, cardio intervals, and accountability coaching to help you achieve lasting transformation.',  # noqa: E501
        'certifications': 'ACE Personal Trainer, Precision Nutrition L1, Behavior Change Specialist',  # noqa: E501
        'years_experience': 5,
        'hourly_rate': 50.00,
        'package_single_rate': 23.00,
        'package_5_rate': 105.00,
        'package_10_rate': 190.00,
        'package_monthly_rate': 170.00,
        'rating': 4.7,
        'total_reviews': 64,
        'location': {'city': 'Birmingham', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/nina_transform',
        'is_verified': True,
        'color': (255, 165, 0),  # Light Orange
    },

    # Yoga (3)
    {
        'username': 'sheena_shah',
        'first_name': 'Sheena',
        'last_name': 'Shah',
        'email': 'sheena.shah@classbooking.com',
        'class_type': 'Yoga',
        'specialties': 'Hatha Yoga, Vinyasa Flow, Flexibility Training, Mindfulness',  # noqa: E501
        'bio': 'Sheena is a certified Hatha Yoga instructor with 8 years of experience teaching in London. She specializes in beginner-friendly classes that focus on flexibility and mindfulness, helping students discover the transformative power of yoga.',  # noqa: E501
        'lesson_description': 'Traditional Hatha yoga combined with modern flexibility training. Each session includes warm-up poses, main asana practice, breathing techniques, and deep relaxation. Perfect for all levels.',  # noqa: E501
        'certifications': 'Yoga Alliance 200-Hour RYT, Certified Yoga Instructor, CPR/First Aid',  # noqa: E501
        'years_experience': 8,
        'hourly_rate': 45.00,
        'package_single_rate': 18.00,
        'package_5_rate': 80.00,
        'package_10_rate': 150.00,
        'package_monthly_rate': 120.00,
        'rating': 4.8,
        'total_reviews': 127,
        'location': {'city': 'London', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/sheena_yoga',
        'is_verified': True,
        'color': (135, 206, 235),  # Sky Blue
    },
    {
        'username': 'priya_sharma',
        'first_name': 'Priya',
        'last_name': 'Sharma',
        'email': 'priya.sharma@classbooking.com',
        'class_type': 'Yoga',
        'specialties': 'Ashtanga Yoga, Power Yoga, Advanced Vinyasa',
        'bio': 'Priya brings 10 years of intensive yoga practice and 6 years of teaching experience. Trained in India, she specializes in Ashtanga and Power Yoga for those seeking a more challenging physical practice.',  # noqa: E501
        'lesson_description': 'Dynamic and challenging yoga flows for intermediate to advanced practitioners. Build strength, stamina, and focus through traditional Ashtanga sequences and powerful vinyasa movements.',  # noqa: E501
        'certifications': 'Yoga Alliance 500-Hour RYT, Ashtanga Authorization, Yoga Therapy Foundation',  # noqa: E501
        'years_experience': 6,
        'hourly_rate': 48.00,
        'package_single_rate': 20.00,
        'package_5_rate': 85.00,
        'package_10_rate': 160.00,
        'package_monthly_rate': 130.00,
        'rating': 4.9,
        'total_reviews': 95,
        'location': {'city': 'Bristol', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/priya_ashtanga',
        'is_verified': True,
        'color': (100, 180, 230),  # Medium Blue
    },
    {
        'username': 'neil_patel',
        'first_name': 'Neil',
        'last_name': 'Patel',
        'email': 'neil.patel@classbooking.com',
        'class_type': 'Yoga',
        'specialties': 'Yin Yoga, Restorative Yoga, Meditation, Stress Relief',
        'bio': 'Neil specializes in gentle yoga styles with 7 years of teaching experience. His focus is on relaxation, flexibility, and stress reduction through slow, mindful practices.',  # noqa: E501
        'lesson_description': 'Gentle restorative and yin yoga classes designed to release tension, improve flexibility, and calm the mind. Each pose is held longer to allow deep relaxation and healing. Perfect for stress relief.',  # noqa: E501
        'certifications': 'Yoga Alliance 200-Hour RYT, Yin Yoga Certified, Meditation Teacher',  # noqa: E501
        'years_experience': 7,
        'hourly_rate': 42.00,
        'package_single_rate': 17.00,
        'package_5_rate': 75.00,
        'package_10_rate': 140.00,
        'package_monthly_rate': 115.00,
        'rating': 4.7,
        'total_reviews': 82,
        'location': {'city': 'Edinburgh', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/neil_yinyoga',
        'is_verified': True,
        'color': (150, 200, 240),  # Light Blue
    },

    # Pilates (2)
    {
        'username': 'emma_watson',
        'first_name': 'Emma',
        'last_name': 'Watson',
        'email': 'emma.watson@classbooking.com',
        'class_type': 'Pilates',
        'specialties': 'Pilates Mat, Pilates Apparatus, Core Strength, Posture Correction',  # noqa: E501
        'bio': 'Emma is a certified Pilates instructor with 5 years of teaching experience, trained at the London Pilates Academy. She specializes in both mat and apparatus-based Pilates, helping clients build core strength and improve posture.',  # noqa: E501
        'lesson_description': 'Core-focused Pilates using controlled, precise movements. Sessions include breathing techniques, flexibility work, and targeted muscle engagement for improved strength, flexibility, and body alignment.',  # noqa: E501
        'certifications': 'CIMSPA Pilates Instructor, Mat Pilates Certified, Yoga Foundation',  # noqa: E501
        'years_experience': 5,
        'hourly_rate': 40.00,
        'package_single_rate': 16.00,
        'package_5_rate': 70.00,
        'package_10_rate': 130.00,
        'package_monthly_rate': 100.00,
        'rating': 4.7,
        'total_reviews': 64,
        'location': {'city': 'London', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/emma_pilates',
        'is_verified': True,
        'color': (200, 100, 200),  # Purple
    },
    {
        'username': 'daniel_sullivan',
        'first_name': 'Daniel',
        'last_name': 'Sullivan',
        'email': 'daniel.sullivan@classbooking.com',
        'class_type': 'Pilates',
        'specialties': 'Reformer Pilates, Clinical Pilates, Rehabilitation',
        'bio': 'Daniel combines 6 years of Pilates instruction with clinical training to help clients recover from injuries and prevent future issues. He specializes in reformer Pilates and therapeutic movement.',  # noqa: E501
        'lesson_description': 'Clinical Pilates sessions using reformer apparatus and mat work. Ideal for injury recovery, chronic pain management, and building functional strength through safe, controlled movements.',  # noqa: E501
        'certifications': 'STOTT Pilates Certified, Clinical Pilates, Physical Therapy Assistant',  # noqa: E501
        'years_experience': 6,
        'hourly_rate': 45.00,
        'package_single_rate': 18.00,
        'package_5_rate': 80.00,
        'package_10_rate': 150.00,
        'package_monthly_rate': 120.00,
        'rating': 4.8,
        'total_reviews': 71,
        'location': {'city': 'Leeds', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/daniel_reformer',
        'is_verified': True,
        'color': (180, 120, 200),  # Light Purple
    },

    # Boxercise (2)
    {
        'username': 'tyler_jones',
        'first_name': 'Tyler',
        'last_name': 'Jones',
        'email': 'tyler.jones@classbooking.com',
        'class_type': 'Boxercise',
        'specialties': 'Kickboxing, Cardio Boxing, Combat Fitness',
        'bio': 'Tyler is a kickboxing and cardio boxing specialist with 7 years of experience. His energetic classes focus on fitness, stress relief, and basic self-defense techniques through boxing and kickboxing movements.',  # noqa: E501
        'lesson_description': 'Fast-paced cardio boxing and kickboxing sessions that burn calories and build confidence. Learn proper striking technique while getting an intense full-body workout. No experience needed.',  # noqa: E501
        'certifications': 'ISKA Kickboxing Instructor, Cardio Boxing Certified, Self-Defense Instructor',  # noqa: E501
        'years_experience': 7,
        'hourly_rate': 48.00,
        'package_single_rate': 19.00,
        'package_5_rate': 85.00,
        'package_10_rate': 160.00,
        'package_monthly_rate': 130.00,
        'rating': 4.7,
        'total_reviews': 88,
        'location': {'city': 'Glasgow', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/tyler_kickboxing',
        'is_verified': True,
        'color': (220, 20, 60),  # Crimson
    },
    {
        'username': 'james_taylor',
        'first_name': 'James',
        'last_name': 'Taylor',
        'email': 'james.taylor@classbooking.com',
        'class_type': 'Boxercise',
        'specialties': 'Boxing Training, Fitness Boxing, Self-Defense, Competitive Boxing',  # noqa: E501
        'bio': 'James is a professional boxing coach with 6 years of competitive and coaching experience. He trains both fitness enthusiasts and competitive boxers, combining traditional boxing drills with modern fitness coaching.',  # noqa: E501
        'lesson_description': 'High-energy boxing classes that blend technical skills with cardiovascular training. Includes pad work, heavy bag training, footwork drills, and combinations for an incredible full-body workout.',  # noqa: E501
        'certifications': 'Professional Boxing Coach, Amateur Boxing Association, NASM Certified',  # noqa: E501
        'years_experience': 6,
        'hourly_rate': 50.00,
        'package_single_rate': 20.00,
        'package_5_rate': 90.00,
        'package_10_rate': 170.00,
        'package_monthly_rate': 140.00,
        'rating': 4.9,
        'total_reviews': 89,
        'location': {'city': 'London', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/james_boxing',
        'is_verified': True,
        'color': (200, 30, 70),  # Dark Red
    },
]


def generate_instructor_image(first_name, last_name, bg_color):
    """Generate professional placeholder profile image."""
    img_size = 400
    img = Image.new('RGB', (img_size, img_size), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw circle
    circle_size = 280
    circle_pos = [(img_size - circle_size) // 2, (img_size - circle_size) // 2,
                  (img_size + circle_size) // 2, (img_size + circle_size) // 2]
    draw.ellipse(circle_pos, fill=(240, 240, 240),
                 outline=(200, 200, 200), width=2)

    # Draw initials
    initials = f"{first_name[0]}{last_name[0]}".upper()
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except BaseException:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (img_size - text_width) // 2
    y = (img_size - text_height) // 2 - 20

    draw.text((x, y), initials, fill=bg_color, font=font)

    # Add name at bottom
    try:
        name_font = ImageFont.truetype("arial.ttf", 24)
    except BaseException:
        name_font = ImageFont.load_default()

    name_text = f"{first_name} {last_name}"
    name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (img_size - name_width) // 2
    draw.text((name_x, img_size - 60), name_text,
              fill=(255, 255, 255), font=name_font)

    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io


def set_if_blank(instance, field_name, value):
    """Set a model field only when it's blank/empty."""
    current_value = getattr(instance, field_name)
    if current_value in (None, ''):
        setattr(instance, field_name, value)
        return True
    return False


def create_10_instructors():
    """Create 10 unique instructors with safe-mode updates for existing records."""  # noqa: E501

    print("\n" + "=" * 80)
    print("CREATING 10 INSTRUCTORS WITH EXCLUSIVE CLASS TYPE ASSIGNMENTS")
    print("=" * 80 + "\n")
    print("Distribution: Personal Trainer (3), Yoga (3), Pilates (2), Boxercise (2)")  # noqa: E501
    print("Each instructor assigned to ONE class type only\n")

    created_count = 0
    updated_count = 0
    unchanged_count = 0

    for data in INSTRUCTORS:
        username = data['username']
        print(
            f"Processing: {data['first_name']} {data['last_name']} "
            f"({data['class_type']})...",
            end=" "
        )

        # Get or create user
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
            }
        )

        # Existing users: fill blank account fields only
        user_changed_fields = []
        if set_if_blank(user, 'email', data['email']):
            user_changed_fields.append('email')
        if set_if_blank(user, 'first_name', data['first_name']):
            user_changed_fields.append('first_name')
        if set_if_blank(user, 'last_name', data['last_name']):
            user_changed_fields.append('last_name')
        if user_changed_fields:
            user.save(update_fields=user_changed_fields)

        # Update user profile with location
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        profile_changed_fields = []
        if set_if_blank(
            user_profile,
            'town_or_city',
                data['location']['city']):
            profile_changed_fields.append('town_or_city')
        if set_if_blank(user_profile, 'country', data['location']['country']):
            profile_changed_fields.append('country')
        if profile_changed_fields:
            user_profile.save(update_fields=profile_changed_fields)

        # Get or create instructor profile
        instructor, created = Instructor.objects.get_or_create(user=user)

        if created:
            # New records receive full dataset
            instructor.bio = data['bio']
            instructor.lesson_description = data['lesson_description']
            instructor.specialties = data['specialties']
            instructor.class_type = data['class_type']
            instructor.certifications = data['certifications']
            instructor.years_experience = data['years_experience']
            instructor.hourly_rate = data['hourly_rate']
            instructor.package_single_rate = data['package_single_rate']
            instructor.package_5_rate = data['package_5_rate']
            instructor.package_10_rate = data['package_10_rate']
            instructor.package_monthly_rate = data['package_monthly_rate']
            instructor.rating = data['rating']
            instructor.total_reviews = data['total_reviews']
            instructor.instagram = data['instagram']
            instructor.is_verified = data['is_verified']
            instructor.is_active = True

            img_io = generate_instructor_image(
                data['first_name'], data['last_name'], data['color'])
            image_name = f"instructor_{username}.png"
            instructor.image.save(
                image_name, ContentFile(img_io.read()), save=False)
            instructor.save()

            created_count += 1
            print("âœ… Created")
        else:
            # Existing records: fill blank fields only
            changed_fields = []
            field_map = {
                'bio': data['bio'],
                'lesson_description': data['lesson_description'],
                'specialties': data['specialties'],
                'class_type': data['class_type'],
                'certifications': data['certifications'],
                'hourly_rate': data['hourly_rate'],
                'package_single_rate': data['package_single_rate'],
                'package_5_rate': data['package_5_rate'],
                'package_10_rate': data['package_10_rate'],
                'package_monthly_rate': data['package_monthly_rate'],
                'rating': data['rating'],
                'instagram': data['instagram'],
            }

            for field_name, field_value in field_map.items():
                if set_if_blank(instructor, field_name, field_value):
                    changed_fields.append(field_name)

            if not instructor.image:
                img_io = generate_instructor_image(
                    data['first_name'], data['last_name'], data['color'])
                image_name = f"instructor_{username}.png"
                instructor.image.save(
                    image_name, ContentFile(img_io.read()), save=False)
                changed_fields.append('image')

            if changed_fields:
                instructor.save(update_fields=changed_fields)
                updated_count += 1
                print("âœ… Updated (blank fields only)")
            else:
                unchanged_count += 1
                print("âœ… No changes (existing values preserved)")

        print(f"   â†’ Class Type: {data['class_type']}")
        print(
            f"   â†’ Location: {
                data['location']['city']}, {
                data['location']['country']}")
        print(f"   â†’ Specialties: {data['specialties']}")
        print()

    print("=" * 80)
    print(
        f"âœ… COMPLETED: {created_count} created, {updated_count} updated, {unchanged_count} unchanged")  # noqa: E501
    print("=" * 80)
    print("\nðŸ“Š Distribution Summary:")
    print("   â€¢ Personal Trainer: 3 instructors")
    print("   â€¢ Yoga: 3 instructors")
    print("   â€¢ Pilates: 2 instructors")
    print("   â€¢ Boxercise: 2 instructors")
    print("   â€¢ TOTAL: 10 instructors\n")
    print("View instructors:")
    print("  â€¢ Classes page: http://127.0.0.1:8000/services/classes/")
    print("  â€¢ Admin panel: http://127.0.0.1:8000/admin/profiles/instructor/")  # noqa: E501


if __name__ == '__main__':
    try:
        create_10_instructors()
    except Exception as e:
        print(f"\nâŒ Error: {e}")
        import traceback
        traceback.print_exc()
