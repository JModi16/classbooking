import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()

from profiles.models import Instructor

# Get Sarah Smith
instructor = Instructor.objects.first()

if instructor:
    print(f"Updating instructor: {instructor.get_display_name()}")
    
    # Update bio with more detail
    instructor.bio = """Sarah is a certified yoga instructor with over 10 years of experience in teaching various yoga styles. Her journey began in India where she completed her 200-hour and 500-hour yoga teacher training certifications.

She specializes in Vinyasa and Hatha yoga, bringing a holistic approach that combines physical postures, breathing techniques, and meditation. Sarah believes in making yoga accessible to everyone, regardless of their fitness level or experience.

Her classes are known for their balanced flow between challenge and relaxation, helping students build strength, flexibility, and inner peace."""
    
    # Add lesson description
    instructor.lesson_description = """Each lesson is designed to provide a complete mind-body experience. Sessions typically begin with gentle warm-ups and breathing exercises, progress through a flowing sequence of postures, and conclude with deep relaxation and meditation.

What you can expect:
• Personalized attention and modifications for all fitness levels
• Focus on proper alignment and breathing techniques
• A welcoming, non-judgmental environment
• Integration of mindfulness and meditation practices
• Progressive difficulty to help you grow at your own pace

All necessary equipment (mats, blocks, straps) is provided. Please wear comfortable clothing that allows freedom of movement and bring water."""
    
    # Update certifications
    instructor.certifications = """- 500-Hour Registered Yoga Teacher (RYT-500)
- 200-Hour Yoga Teacher Training Certificate
- Prenatal Yoga Certification
- Yin Yoga Specialist
- Meditation & Mindfulness Instructor
- First Aid & CPR Certified"""
    
    # Set rating and rates
    instructor.rating = 4.8
    instructor.total_reviews = 47
    instructor.hourly_rate = 60.00
    
    # Set package pricing
    instructor.package_single_rate = 25.00
    instructor.package_5_rate = 110.00  # £22 per session
    instructor.package_10_rate = 200.00  # £20 per session - best value
    instructor.package_monthly_rate = 150.00  # Unlimited
    
    # Update specialties
    instructor.specialties = "Vinyasa Yoga, Hatha Yoga, Yin Yoga, Prenatal Yoga, Meditation, Breathwork"
    
    # Mark as verified
    instructor.is_verified = True
    
    # Update instagram
    instructor.instagram = "https://instagram.com/sarahyoga"
    
    instructor.save()
    
    print("✅ Instructor updated successfully!")
    print(f"   Rating: {instructor.rating} ({instructor.total_reviews} reviews)")
    print(f"   Hourly Rate: £{instructor.hourly_rate}")
    print(f"   Package Rates:")
    print(f"     - Single: £{instructor.package_single_rate}")
    print(f"     - 5 Pack: £{instructor.package_5_rate} (£{instructor.package_5_rate/5:.2f}/session)")
    print(f"     - 10 Pack: £{instructor.package_10_rate} (£{instructor.package_10_rate/10:.2f}/session)")
    print(f"     - Monthly: £{instructor.package_monthly_rate} (unlimited)")
    print(f"   Verified: {instructor.is_verified}")
    print(f"   Lesson Description: Added ✓")
else:
    print("❌ No instructor found")
