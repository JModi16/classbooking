import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()

from profiles.models import Instructor

instructor = Instructor.objects.first()
if instructor:
    print(f"Instructor ID: {instructor.id}")
    print(f"URL: /services/instructor/{instructor.id}/")
