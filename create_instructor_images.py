import os
import django
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()

from profiles.models import Instructor

# Ensure media directory exists
media_instructors_dir = os.path.join('media', 'instructors')
os.makedirs(media_instructors_dir, exist_ok=True)

# Get Sarah Smith
instructor = Instructor.objects.first()

if instructor:
    print(f"Creating professional image for: {instructor.get_display_name()}")
    
    # Create a more professional looking placeholder image
    # Light blue gradient background (matching our site theme)
    img = Image.new('RGB', (400, 400), color='#87CEEB')
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect (light blue to sky blue)
    for i in range(400):
        # Gradient from light blue to darker blue
        r = int(135 + (27 - 135) * (i / 400))
        g = int(206 + (78 - 206) * (i / 400))
        b = int(235)
        color = (r, g, b)
        draw.line([(0, i), (400, i)], fill=color)
    
    # Draw a circle for the head area
    draw.ellipse([75, 50, 325, 300], fill='#FFD9B3', outline='#DAA76F', width=3)
    
    # Draw shoulders area (trapezoid effect with rectangles)
    draw.rectangle([100, 250, 300, 400], fill='#4A90E2')
    
    # Add initials
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()
    
    initials = f"{instructor.user.first_name[0]}{instructor.user.last_name[0]}"
    
    # Get text bounding box to center it
    text_bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (400 - text_width) // 2
    y = (150 - text_height) // 2
    
    draw.text((x, y), initials, fill='#003d82', font=font)
    
    # Save the image directly to file system
    filename = f'{instructor.user.username}_profile.jpg'
    filepath = os.path.join(media_instructors_dir, filename)
    img.save(filepath, format='JPEG', quality=95)
    
    # Update the database record to point to this image
    instructor.image = f'instructors/{filename}'
    instructor.save()
    
    print(f"✅ Image created and saved for {instructor.get_display_name()}")
    print(f"   File: {filepath}")
    print(f"   Database path: {instructor.image}")
else:
    print("❌ No instructor found")
