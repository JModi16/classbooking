from django.contrib.auth.models import User
from profiles.models import Instructor
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_platform.settings')
django.setup()


print("=== ALL INSTRUCTORS ===")
instructors = Instructor.objects.all()
print(f"Total Instructor records: {instructors.count()}")
for i, inst in enumerate(instructors, 1):
    print(
        f"{i}. {inst.get_display_name()} (ID: {inst.id}) "
        f"- User: {inst.user.id}"
    )

print("\n=== ALL USERS ===")
users_with_instructor = User.objects.filter(instructor_profile__isnull=False)
print(f"Users with instructor profile: {users_with_instructor.count()}")
for user in users_with_instructor:
    print(f"- {user.get_full_name()} (ID: {user.id})")
