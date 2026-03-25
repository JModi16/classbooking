from django.contrib import admin
from datetime import timedelta
from .models import Service, Category, ExerciseClass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "friendly_name")
    search_fields = ("name",)


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "duration_minutes",
        "available",
    )
    list_filter = ("category", "available", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")


class ExerciseClassAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "instructor",
        "category",
        "start_datetime",
        "get_available_spots",
        "max_participants",
        "price",
        "available",
    )
    list_filter = (
        "category",
        "difficulty_level",
        "available",
        "instructor",
        "start_datetime",
    )
    search_fields = (
        "name",
        "description",
        "instructor__user__first_name",
        "instructor__user__last_name",
    )
    readonly_fields = ("created_at", "updated_at")
    actions = ("duplicate_selected_classes",)
    fieldsets = (
        (
            "Class Info",
            {
                "fields": (
                    "name",
                    "description",
                    "category",
                    "instructor",
                    "difficulty_level",
                )
            },
        ),
        (
            "Schedule & Capacity",
            {"fields": ("start_datetime", "end_datetime", "max_participants")},
        ),
        ("Pricing & Media", {"fields": ("price", "image_url", "image")}),
        ("Status", {"fields": ("available",)}),
        (
            "Tracking",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_available_spots(self, obj):
        return obj.get_available_spots()

    get_available_spots.short_description = "Available Spots"

    @admin.action(description="Duplicate selected classes (+7 days)")
    def duplicate_selected_classes(self, request, queryset):
        duplicated_count = 0
        for exercise_class in queryset:
            exercise_class.pk = None
            exercise_class.start_datetime = (
                exercise_class.start_datetime + timedelta(days=7)
            )
            exercise_class.end_datetime = (
                exercise_class.end_datetime + timedelta(days=7)
            )
            exercise_class.save()
            duplicated_count += 1

        self.message_user(
            request,
            f"{duplicated_count} class(es) duplicated "
            "with schedule shifted by 7 days.",
        )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ExerciseClass, ExerciseClassAdmin)
