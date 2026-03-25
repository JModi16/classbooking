from django import forms
from django.contrib import admin
from .models import UserProfile, Instructor
from services.models import Category


class InstructorAdminForm(forms.ModelForm):
    class_type = forms.ChoiceField(required=False)

    class Meta:
        model = Instructor
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_choices = [("", "---------")] + [
            (category.name, category.name)
            for category in Category.objects.order_by("name")
        ]

        current_value = (
            self.instance.class_type
            if self.instance and self.instance.pk
            else ""
        )
        if current_value and current_value not in {
            value for value, _label in category_choices
        }:
            category_choices.append((current_value, current_value))

        self.fields["class_type"].choices = category_choices


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "town_or_city", "country")
    list_filter = ("country", "created_at")
    search_fields = ("user__username", "phone_number", "postcode")
    readonly_fields = ("created_at", "updated_at")


class InstructorAdmin(admin.ModelAdmin):
    form = InstructorAdminForm
    list_display = (
        "get_name",
        "class_type",
        "is_verified",
        "years_experience",
        "rating",
        "total_reviews",
        "is_active",
    )
    list_filter = (
        "is_verified",
        "is_active",
        "created_at",
        "years_experience",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "specialties",
        "class_type",
    )
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("User Info", {"fields": ("user",)}),
        (
            "Professional Info",
            {
                "fields": (
                    "bio",
                    "class_type",
                    "specialties",
                    "certifications",
                    "years_experience",
                )
            },
        ),
        ("Rating & Reviews", {"fields": ("rating", "total_reviews")}),
        (
            "Rates & Packages",
            {
                "fields": (
                    "hourly_rate",
                    "package_single_rate",
                    "package_5_rate",
                    "package_10_rate",
                    "package_monthly_rate",
                )
            },
        ),
        ("Media & Contact", {"fields": ("image", "phone", "instagram")}),
        ("Status", {"fields": ("is_active", "is_verified")}),
        (
            "Tracking",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_name(self, obj):
        return obj.get_display_name()

    get_name.short_description = "Instructor Name"


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Instructor, InstructorAdmin)
