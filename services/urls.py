from django.urls import path
from . import views

urlpatterns = [
    # Legacy services paths
    path('', views.all_services, name='services'),
    path('search/', views.site_search, name='site_search'),
    path('<int:service_id>/', views.service_detail, name='service_detail'),
    
    # Exercise class paths
    path('classes/', views.all_classes, name='classes'),
    path('classes/<int:class_id>/', views.class_detail, name='class_detail'),
    
    # Instructor paths
    path('instructors/', views.all_instructors, name='instructors'),
    path('instructor/<int:instructor_id>/', views.instructor_profile, name='instructor_profile'),
]
