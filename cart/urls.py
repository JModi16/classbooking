from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    # Legacy service cart paths
    path("add/<int:service_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "remove/<int:service_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    # Exercise class booking paths
    path(
        "add-class/<int:class_id>/",
        views.add_class_to_cart,
        name="add_class_to_cart",
    ),
    path(
        "remove-class/<int:class_id>/",
        views.remove_from_cart,
        name="remove_class_from_cart",
    ),
    path(
        "update-quantity/<int:class_id>/",
        views.update_quantity,
        name="update_quantity",
    ),
    # Instructor package booking paths
    path(
        "add-package/<int:instructor_id>/<str:package_type>/",
        views.add_package_to_cart,
        name="add_package_to_cart",
    ),
    path(
        "remove-package/<int:instructor_id>/<str:package_type>/",
        views.remove_package_from_cart,
        name="remove_package_from_cart",
    ),
]
