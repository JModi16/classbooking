from django.contrib import admin
from .models import Service, Category


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration_minutes', 'available')
    list_filter = ('category', 'available', 'created_at')
    search_fields = ('name', 'description')


admin.site.register(Service, ServiceAdmin)
admin.site.register(Category)
