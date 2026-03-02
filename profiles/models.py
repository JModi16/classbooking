from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    """User profile for storing delivery/booking information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    
    # Contact Information
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Address Information
    street_address1 = models.CharField(max_length=80, blank=True)
    street_address2 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    county = models.CharField(max_length=80, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=40, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"Profile for {self.user.username}"


class Instructor(models.Model):
    """Personal fitness instructor profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    
    # Basic Info
    bio = models.TextField(blank=True, help_text="Professional biography")
    specialties = models.CharField(max_length=500, blank=True, help_text="Comma-separated specialties (e.g., Yoga, Pilates, HIIT)")
    
    # Qualifications
    certifications = models.TextField(blank=True, help_text="Professional certifications and qualifications")
    years_experience = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Rating & Reviews
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Average rating (0-5 stars)"
    )
    total_reviews = models.IntegerField(default=0)
    
    # Media
    image = models.ImageField(
        null=True, 
        blank=True,
        help_text="Professional photo"
    )
    
    # Contact & Social
    phone = models.CharField(max_length=20, blank=True)
    instagram = models.URLField(blank=True, help_text="Instagram profile URL")
    
    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False, help_text="Admin verified instructor")
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_verified', '-rating']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - Instructor"

    def get_display_name(self):
        return self.user.get_full_name() or self.user.username

    def get_average_rating(self):
        return self.rating or 0.0
