from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Category(models.Model):
    """Exercise class categories (Yoga, Pilates, HIIT, etc.)"""

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class ExerciseClass(models.Model):
    """Exercise classes that users can book with personal instructors"""

    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="exercise_classes",
    )
    instructor = models.ForeignKey(
        "profiles.Instructor", on_delete=models.PROTECT, related_name="classes"
    )

    # Basic Info
    name = models.CharField(max_length=254)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default="intermediate"
    )

    # Scheduling
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    # Capacity
    max_participants = models.IntegerField(default=1)

    # Pricing
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Images & Media
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    # Status
    available = models.BooleanField(default=True)

    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_datetime"]
        indexes = [
            models.Index(fields=["start_datetime"]),
            models.Index(fields=["instructor"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{
            self.name} - {
            self.start_datetime.strftime('%Y-%m-%d %H:%M')}"

    def get_available_spots(self):
        """Get number of available spots"""
        booked_count = self.bookings.filter(status="confirmed").count()
        return max(0, self.max_participants - booked_count)

    def is_full(self):
        """Check if class is full"""
        return self.get_available_spots() <= 0

    def is_upcoming(self):
        """Check if class is in the future"""
        return self.start_datetime > timezone.now()

    def get_schedule_options(self):
        """Return upcoming sessions for the same class/instructor."""
        schedule_options = ExerciseClass.objects.filter(
            instructor=self.instructor,
            name=self.name,
            start_datetime__gte=timezone.now(),
        )

        if self.category_id:
            schedule_options = schedule_options.filter(category=self.category)
        else:
            schedule_options = schedule_options.filter(category__isnull=True)

        return schedule_options.select_related(
            "category", "instructor"
        ).order_by("start_datetime")

    def get_schedule_label(self):
        """Return a readable schedule label for template display."""
        return self.start_datetime.strftime("%A, %B %d, %Y at %I:%M %p")

    def clean(self):
        """Validate that end_datetime is after start_datetime"""
        if self.end_datetime <= self.start_datetime:
            raise ValidationError("End time must be after start time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# Keep Service model for backward compatibility if needed
class Service(models.Model):
    """Generic service model (deprecated - use ExerciseClass instead)"""

    category = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    duration_minutes = models.IntegerField(default=60)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
