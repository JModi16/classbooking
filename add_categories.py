import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()

from services.models import Category

# Check existing categories
print("=== EXISTING CATEGORIES ===")
existing = Category.objects.all()
for cat in existing:
    print(f"- {cat.name} (friendly: {cat.get_friendly_name()})")

print("\n=== ADDING NEW CATEGORIES ===")

# New categories to add
new_categories = [
    ('Personal Trainer', 'Personal Trainer'),
    ('Pilates', 'Pilates'),
    ('Boxercise', 'Boxercise'),
]

for name, friendly_name in new_categories:
    category, created = Category.objects.get_or_create(
        name=name,
        defaults={'friendly_name': friendly_name}
    )
    if created:
        print(f"✅ Created: {name}")
    else:
        print(f"⚠️  Already exists: {name}")

print("\n=== ALL CATEGORIES NOW ===")
all_cats = Category.objects.all()
for cat in all_cats:
    print(f"- {cat.name}")
