import os
import sys
import django
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Setup Django
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'service_platform.settings',
)
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

# Instructor data with bios and descriptions
INSTRUCTORS_DATA = [
    {
        'username': 'james_taylor',
        'first_name': 'James',
        'last_name': 'Taylor',
        'email': 'james@example.com',
        'bio': (
            'James is a certified personal trainer and fitness coach with 6 '
            'years of professional experience. He specializes in strength '
            'training, HIIT workouts, and functional fitness. James has '
            'worked with clients ranging from beginners to competitive '
            'athletes, helping them achieve their fitness goals through '
            'personalized training programs.'
        ),
        'lesson_description': (
            'My personal training sessions are tailored to your specific '
            'goals and fitness level. Whether you want to build strength, '
            'lose weight, or improve overall fitness, I create customized '
            'workout plans that keep you motivated and challenged. Sessions '
            'include warm-up, strength/cardio training, and cool-down '
            'stretching.'
        ),
        'specialties': (
            'Strength Training, HIIT, Weight Loss, Functional Fitness'
        ),
        'certifications': (
            'NASM Certified Personal Trainer, CPR/AED, Nutrition Specialist'
        ),
        'years_experience': 6,
        'hourly_rate': 55.00,
        'package_single_rate': 25.00,
        'package_5_rate': 110.00,
        'package_10_rate': 200.00,
        'package_monthly_rate': 180.00,
        'rating': 4.9,
        'total_reviews': 89,
        'instagram': 'https://instagram.com/james_fitness',
        'is_verified': True,
    },
    {
        'username': 'emma_watson',
        'first_name': 'Emma',
        'last_name': 'Watson',
        'email': 'emma@example.com',
        'bio': (
            'Emma is a certified Pilates instructor with 5 years of '
            'teaching experience. She trained at the London Pilates Academy '
            'and specializes in both mat and apparatus-based Pilates. Emma '
            'is passionate about helping her clients build core strength, '
            'improve posture, and achieve better body awareness through '
            'controlled movements.'
        ),
        'lesson_description': (
            'My Pilates classes focus on core strengthening through '
            'controlled, precise movements. Each session includes breathing '
            'techniques, flexibility work, and targeted muscle engagement. '
            'Whether you\'re new to Pilates or looking to deepen your '
            'practice, my classes are designed to improve your strength, '
            'flexibility, and body alignment.'
        ),
        'specialties': (
            'Pilates Mat, Pilates Apparatus, Core Strength, Posture '
            'Correction'
        ),
        'certifications': (
            'CIMSPA Pilates Instructor, Mat Pilates Certified, Yoga '
            'Foundation'
        ),
        'years_experience': 5,
        'hourly_rate': 40.00,
        'package_single_rate': 16.00,
        'package_5_rate': 70.00,
        'package_10_rate': 130.00,
        'package_monthly_rate': 100.00,
        'rating': 4.7,
        'total_reviews': 64,
        'instagram': 'https://instagram.com/emma_pilates',
        'is_verified': True,
    },
    {
        'username': 'mike_anderson',
        'first_name': 'Mike',
        'last_name': 'Anderson',
        'email': 'mike@example.com',
        'bio': (
            'Mike is a professional boxing coach with 10 years of '
            'competitive and coaching experience. He\'s trained multiple '
            'amateur and semi-professional boxers and specializes in '
            'teaching both fitness boxing and competitive technique. Mike '
            'combines traditional boxing drills with modern fitness coaching '
            'to deliver high-energy, effective workouts.'
        ),
        'lesson_description': (
            'My boxing classes blend technical boxing skills with intense '
            'cardiovascular training. Each session includes pad work, heavy '
            'bag training, footwork drills, and combinations. Whether '
            'you\'re training for fitness or competition, my classes '
            'deliver an incredible full-body workout while teaching proper '
            'boxing technique and self-defense skills.'
        ),
        'specialties': (
            'Boxing Training, Fitness Boxing, Self-Defense, Competitive '
            'Boxing'
        ),
        'certifications': (
            'Professional Boxing Coach, Amateur Boxing Association, First '
            'Aid Certified'
        ),
        'years_experience': 10,
        'hourly_rate': 50.00,
        'package_single_rate': 20.00,
        'package_5_rate': 90.00,
        'package_10_rate': 170.00,
        'package_monthly_rate': 140.00,
        'rating': 4.6,
        'total_reviews': 102,
        'instagram': 'https://instagram.com/mike_boxing',
        'is_verified': True,
    },
]


def generate_placeholder_image(first_name, last_name, color_scheme=None):
    """
    Generate a professional-looking placeholder profile image.

    Args:
        first_name: Instructor's first name
        last_name: Instructor's last name
        color_scheme: Optional tuple of (R, G, B) for background color

    Returns:
        BytesIO object containing PNG image data
    """
    # Color schemes for different instructors
    colors = {
        'sarah': (135, 206, 235),      # Sky blue (Yoga)
        'james': (255, 140, 0),         # Dark orange (Personal Training)
        'emma': (200, 100, 200),        # Purple (Pilates)
        'mike': (220, 20, 60),          # Crimson (Boxing)
    }

    # Select color based on first name
    first_lower = first_name.lower()
    bg_color = colors.get(first_lower, (100, 150, 200))

    # Create image
    img_size = 400
    img = Image.new('RGB', (img_size, img_size), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw circle for face
    circle_size = 280
    circle_pos = [(img_size - circle_size) // 2, (img_size - circle_size) // 2,
                  (img_size + circle_size) // 2, (img_size + circle_size) // 2]
    draw.ellipse(circle_pos, fill=(240, 240, 240),
                 outline=(200, 200, 200), width=2)

    # Draw initials
    initials = f"{first_name[0]}{last_name[0]}".upper()
    try:
        # Try to use a larger font
        font_size = 120
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        # Fallback to default font
        font = ImageFont.load_default()

    # Draw text in center
    text_bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (img_size - text_width) // 2
    y = (img_size - text_height) // 2 - 20

    draw.text((x, y), initials, fill=bg_color, font=font)

    # Add name at bottom
    try:
        name_font = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        name_font = ImageFont.load_default()

    name_text = f"{first_name} {last_name}"
    name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (img_size - name_width) // 2
    draw.text((name_x, img_size - 60), name_text,
              fill=(255, 255, 255), font=name_font)

    # Convert to bytes
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


def populate_instructors():
    """Populate instructors in safe mode.

    Existing records only have blank fields filled.
    """

    from django.contrib.auth.models import User
    from django.core.files.base import ContentFile

    from profiles.models import Instructor

    print("\n" + "="*70)
    print("POPULATING INSTRUCTOR DATA AND IMAGES")
    print("="*70 + "\n")

    created_count = 0
    updated_count = 0
    unchanged_count = 0

    for data in INSTRUCTORS_DATA:
        username = data['username']
        full_name = f"{data['first_name']} {data['last_name']}"
        print(f"Processing: {full_name}...", end=" ")

        # Get or create user
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
            }
        )

        if user_created:
            print(f"(new user)", end=" → ")
        else:
            print(f"(existing user)", end=" → ")

        # Safe mode for existing user data
        user_changed_fields = []
        if set_if_blank(user, 'email', data['email']):
            user_changed_fields.append('email')
        if set_if_blank(user, 'first_name', data['first_name']):
            user_changed_fields.append('first_name')
        if set_if_blank(user, 'last_name', data['last_name']):
            user_changed_fields.append('last_name')
        if user_changed_fields:
            user.save(update_fields=user_changed_fields)

        # Get or create instructor profile
        instructor, created = Instructor.objects.get_or_create(user=user)

        changed_fields = []
        if created:
            # New records receive full dataset
            instructor.bio = data['bio']
            instructor.lesson_description = data['lesson_description']
            instructor.specialties = data['specialties']
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

            img_io = generate_placeholder_image(
                data['first_name'], data['last_name']
            )
            image_name = f"instructor_{username}.png"
            instructor.image.save(
                image_name,
                ContentFile(img_io.read()),
                save=False
            )
            print(
                "✅ Created\n"
                "   → Full profile created\n"
                "   → Profile image generated"
            )
            instructor.save()
            created_count += 1
        else:
            # Existing records: fill blank fields only
            field_map = {
                'bio': data['bio'],
                'lesson_description': data['lesson_description'],
                'specialties': data['specialties'],
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
                img_io = generate_placeholder_image(
                    data['first_name'], data['last_name'])
                image_name = f"instructor_{username}.png"
                instructor.image.save(
                    image_name, ContentFile(img_io.read()), save=False)
                changed_fields.append('image')

            if changed_fields:
                instructor.save(update_fields=changed_fields)
                updated_count += 1
                print("✅ Updated (blank fields only)")
                print("   → Existing Admin values preserved")
            else:
                unchanged_count += 1
                print("✅ No changes (existing values preserved)")
        print()

    print("="*70)
    print("✅ ALL INSTRUCTORS POPULATED SUCCESSFULLY")
    print("="*70)
    print(
        f"\nSummary: {created_count} created, "
        f"{updated_count} updated, "
        f"{unchanged_count} unchanged"
    )
    print("\nInstructor profiles are now live on the platform:")
    print("  • Visit: http://127.0.0.1:8000/services/")
    print(
        "  • Admin: http://127.0.0.1:8000/admin/profiles/instructor/"
    )
    print(
        "\nStorage location depends on USE_AWS setting "
        "(S3 when enabled, local media folder otherwise)."
    )


if __name__ == '__main__':
    try:
        populate_instructors()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
