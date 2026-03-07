"""
Create 10 unique instructors, each assigned to exactly one class type.
Distribution: Personal Trainer (3), Yoga (3), Pilates (2), Boxercise (2)
Each instructor has specialties that match only their assigned class type.
"""

import os
import sys
import django
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from profiles.models import Instructor, UserProfile
from django.core.files.base import ContentFile

# 10 instructors with exclusive class type assignments
INSTRUCTORS = [
    # Personal Trainer (3)
    {
        'username': 'james_taylor',
        'first_name': 'James',
        'last_name': 'Taylor',
        'email': 'james.taylor@classbooking.com',
        'class_type': 'Personal Trainer',
        'specialties': 'Strength Training, HIIT, Weight Loss, Functional Fitness',
        'bio': 'James is a certified personal trainer with 6 years of experience specializing in strength training and HIIT workouts. He has helped clients achieve dramatic transformations through personalized training programs.',
        'lesson_description': 'Customized personal training sessions focused on your specific goals. Each session includes warm-up, targeted strength/cardio work, and proper cool-down. Perfect for weight loss, muscle building, or overall fitness improvement.',
        'certifications': 'NASM Certified Personal Trainer, CPR/AED, Nutrition Specialist',
        'years_experience': 6,
        'hourly_rate': 55.00,
        'package_single_rate': 25.00,
        'package_5_rate': 110.00,
        'package_10_rate': 200.00,
        'package_monthly_rate': 180.00,
        'rating': 4.9,
        'total_reviews': 89,
        'location': {'city': 'London', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/james_fitness',
        'is_verified': True,
        'color': (255, 140, 0),  # Orange
    },
    {
        'username': 'marcus_reid',
        'first_name': 'Marcus',
        'last_name': 'Reid',
        'email': 'marcus.reid@classbooking.com',
        'class_type': 'Personal Trainer',
        'specialties': 'Athletic Performance, Sports Conditioning, Injury Prevention',
        'bio': 'Marcus specializes in athletic performance and sports conditioning with 8 years of experience training competitive athletes. His focus is on improving speed, agility, and preventing injuries.',
        'lesson_description': 'High-performance training for athletes looking to excel in their sport. Sessions emphasize explosive power, speed development, and injury prevention through proper movement mechanics.',
        'certifications': 'ISSA Elite Trainer, Sports Performance Specialist, Corrective Exercise',
        'years_experience': 8,
        'hourly_rate': 60.00,
        'package_single_rate': 28.00,
        'package_5_rate': 125.00,
        'package_10_rate': 220.00,
        'package_monthly_rate': 200.00,
        'rating': 4.8,
        'total_reviews': 76,
        'location': {'city': 'Manchester', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/marcus_performance',
        'is_verified': True,
        'color': (220, 100, 40),  # Dark Orange
    },
    {
        'username': 'nina_foster',
        'first_name': 'Nina',
        'last_name': 'Foster',
        'email': 'nina.foster@classbooking.com',
        'class_type': 'Personal Trainer',
        'specialties': 'Weight Management, Metabolic Training, Body Transformation',
        'bio': 'Nina is a transformation specialist with 5 years of experience helping clients achieve sustainable weight loss and body composition changes through evidence-based training and lifestyle coaching.',
        'lesson_description': 'Results-driven personal training focused on fat loss and metabolic health. Combines resistance training, cardio intervals, and accountability coaching to help you achieve lasting transformation.',
        'certifications': 'ACE Personal Trainer, Precision Nutrition L1, Behavior Change Specialist',
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
        'username': 'sarah_smith',
        'first_name': 'Sarah',
        'last_name': 'Smith',
        'email': 'sarah.smith@classbooking.com',
        'class_type': 'Yoga',
        'specialties': 'Hatha Yoga, Vinyasa Flow, Flexibility Training, Mindfulness',
        'bio': 'Sarah is a certified Hatha Yoga instructor with 8 years of experience teaching in London. She specializes in beginner-friendly classes that focus on flexibility and mindfulness, helping students discover the transformative power of yoga.',
        'lesson_description': 'Traditional Hatha yoga combined with modern flexibility training. Each session includes warm-up poses, main asana practice, breathing techniques, and deep relaxation. Perfect for all levels.',
        'certifications': 'Yoga Alliance 200-Hour RYT, Certified Yoga Instructor, CPR/First Aid',
        'years_experience': 8,
        'hourly_rate': 45.00,
        'package_single_rate': 18.00,
        'package_5_rate': 80.00,
        'package_10_rate': 150.00,
        'package_monthly_rate': 120.00,
        'rating': 4.8,
        'total_reviews': 127,
        'location': {'city': 'London', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/sarah_yoga',
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
        'bio': 'Priya brings 10 years of intensive yoga practice and 6 years of teaching experience. Trained in India, she specializes in Ashtanga and Power Yoga for those seeking a more challenging physical practice.',
        'lesson_description': 'Dynamic and challenging yoga flows for intermediate to advanced practitioners. Build strength, stamina, and focus through traditional Ashtanga sequences and powerful vinyasa movements.',
        'certifications': 'Yoga Alliance 500-Hour RYT, Ashtanga Authorization, Yoga Therapy Foundation',
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
        'username': 'lily_chen',
        'first_name': 'Lily',
        'last_name': 'Chen',
        'email': 'lily.chen@classbooking.com',
        'class_type': 'Yoga',
        'specialties': 'Yin Yoga, Restorative Yoga, Meditation, Stress Relief',
        'bio': 'Lily specializes in gentle yoga styles with 7 years of teaching experience. Her focus is on relaxation, flexibility, and stress reduction through slow, mindful practices.',
        'lesson_description': 'Gentle restorative and yin yoga classes designed to release tension, improve flexibility, and calm the mind. Each pose is held longer to allow deep relaxation and healing. Perfect for stress relief.',
        'certifications': 'Yoga Alliance 200-Hour RYT, Yin Yoga Certified, Meditation Teacher',
        'years_experience': 7,
        'hourly_rate': 42.00,
        'package_single_rate': 17.00,
        'package_5_rate': 75.00,
        'package_10_rate': 140.00,
        'package_monthly_rate': 115.00,
        'rating': 4.7,
        'total_reviews': 82,
        'location': {'city': 'Edinburgh', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/lily_yinyoga',
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
        'specialties': 'Pilates Mat, Pilates Apparatus, Core Strength, Posture Correction',
        'bio': 'Emma is a certified Pilates instructor with 5 years of teaching experience, trained at the London Pilates Academy. She specializes in both mat and apparatus-based Pilates, helping clients build core strength and improve posture.',
        'lesson_description': 'Core-focused Pilates using controlled, precise movements. Sessions include breathing techniques, flexibility work, and targeted muscle engagement for improved strength, flexibility, and body alignment.',
        'certifications': 'CIMSPA Pilates Instructor, Mat Pilates Certified, Yoga Foundation',
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
        'username': 'olivia_grant',
        'first_name': 'Olivia',
        'last_name': 'Grant',
        'email': 'olivia.grant@classbooking.com',
        'class_type': 'Pilates',
        'specialties': 'Reformer Pilates, Clinical Pilates, Rehabilitation',
        'bio': 'Olivia combines 6 years of Pilates instruction with clinical training to help clients recover from injuries and prevent future issues. She specializes in reformer Pilates and therapeutic movement.',
        'lesson_description': 'Clinical Pilates sessions using reformer apparatus and mat work. Ideal for injury recovery, chronic pain management, and building functional strength through safe, controlled movements.',
        'certifications': 'STOTT Pilates Certified, Clinical Pilates, Physical Therapy Assistant',
        'years_experience': 6,
        'hourly_rate': 45.00,
        'package_single_rate': 18.00,
        'package_5_rate': 80.00,
        'package_10_rate': 150.00,
        'package_monthly_rate': 120.00,
        'rating': 4.8,
        'total_reviews': 71,
        'location': {'city': 'Leeds', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/olivia_reformer',
        'is_verified': True,
        'color': (180, 120, 200),  # Light Purple
    },
    
    # Boxercise (2)
    {
        'username': 'mike_anderson',
        'first_name': 'Mike',
        'last_name': 'Anderson',
        'email': 'mike.anderson@classbooking.com',
        'class_type': 'Boxercise',
        'specialties': 'Boxing Training, Fitness Boxing, Self-Defense, Competitive Boxing',
        'bio': 'Mike is a professional boxing coach with 10 years of competitive and coaching experience. He trains both fitness enthusiasts and competitive boxers, combining traditional boxing drills with modern fitness coaching.',
        'lesson_description': 'High-energy boxing classes that blend technical skills with cardiovascular training. Includes pad work, heavy bag training, footwork drills, and combinations for an incredible full-body workout.',
        'certifications': 'Professional Boxing Coach, Amateur Boxing Association, First Aid Certified',
        'years_experience': 10,
        'hourly_rate': 50.00,
        'package_single_rate': 20.00,
        'package_5_rate': 90.00,
        'package_10_rate': 170.00,
        'package_monthly_rate': 140.00,
        'rating': 4.6,
        'total_reviews': 102,
        'location': {'city': 'Liverpool', 'country': 'United Kingdom'},
        'instagram': 'https://instagram.com/mike_boxing',
        'is_verified': True,
        'color': (220, 20, 60),  # Crimson
    },
    {
        'username': 'tyler_jones',
        'first_name': 'Tyler',
        'last_name': 'Jones',
        'email': 'tyler.jones@classbooking.com',
        'class_type': 'Boxercise',
        'specialties': 'Kickboxing, Cardio Boxing, Combat Fitness',
        'bio': 'Tyler is a kickboxing and cardio boxing specialist with 7 years of experience. His energetic classes focus on fitness, stress relief, and basic self-defense techniques through boxing and kickboxing movements.',
        'lesson_description': 'Fast-paced cardio boxing and kickboxing sessions that burn calories and build confidence. Learn proper striking technique while getting an intense full-body workout. No experience needed.',
        'certifications': 'ISKA Kickboxing Instructor, Cardio Boxing Certified, Self-Defense Instructor',
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
    draw.ellipse(circle_pos, fill=(240, 240, 240), outline=(200, 200, 200), width=2)
    
    # Draw initials
    initials = f"{first_name[0]}{last_name[0]}".upper()
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
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
    except:
        name_font = ImageFont.load_default()
    
    name_text = f"{first_name} {last_name}"
    name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (img_size - name_width) // 2
    draw.text((name_x, img_size - 60), name_text, fill=(255, 255, 255), font=name_font)
    
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io


def create_10_instructors():
    """Create 10 unique instructors with exclusive class type assignments."""
    
    print("\n" + "="*80)
    print("CREATING 10 INSTRUCTORS WITH EXCLUSIVE CLASS TYPE ASSIGNMENTS")
    print("="*80 + "\n")
    print("Distribution: Personal Trainer (3), Yoga (3), Pilates (2), Boxercise (2)")
    print("Each instructor assigned to ONE class type only\n")
    
    created_count = 0
    updated_count = 0
    
    for data in INSTRUCTORS:
        username = data['username']
        print(f"Processing: {data['first_name']} {data['last_name']} ({data['class_type']})...", end=" ")
        
        # Get or create user
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
            }
        )
        
        # Update user profile with location
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        user_profile.town_or_city = data['location']['city']
        user_profile.country = data['location']['country']
        user_profile.save()
        
        # Get or create instructor profile
        instructor, created = Instructor.objects.get_or_create(user=user)
        
        # Update all fields
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
        
        # Generate and save image
        img_io = generate_instructor_image(data['first_name'], data['last_name'], data['color'])
        image_name = f"instructor_{username}.png"
        instructor.image.save(image_name, ContentFile(img_io.read()), save=False)
        
        instructor.save()
        
        if created:
            created_count += 1
            print(f"✅ Created")
        else:
            updated_count += 1
            print(f"✅ Updated")
        
        print(f"   → Class Type: {data['class_type']}")
        print(f"   → Location: {data['location']['city']}, {data['location']['country']}")
        print(f"   → Specialties: {data['specialties']}")
        print()
    
    print("="*80)
    print(f"✅ COMPLETED: {created_count} created, {updated_count} updated")
    print("="*80)
    print("\n📊 Distribution Summary:")
    print("   • Personal Trainer: 3 instructors")
    print("   • Yoga: 3 instructors")
    print("   • Pilates: 2 instructors")
    print("   • Boxercise: 2 instructors")
    print("   • TOTAL: 10 instructors\n")
    print("View instructors:")
    print("  • Classes page: http://127.0.0.1:8000/services/classes/")
    print("  • Admin panel: http://127.0.0.1:8000/admin/profiles/instructor/")


if __name__ == '__main__':
    try:
        create_10_instructors()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
