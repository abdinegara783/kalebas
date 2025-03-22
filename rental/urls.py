from django.urls import path
from . import views

urlpatterns = [
    # Customer-facing URLs
    path("", views.home, name="home"),
    path("booking/", views.booking_page, name="booking"),
    path(
        "booking-confirmation/<int:booking_id>/",
        views.booking_confirmation,
        name="booking_confirmation",
    ),
    path("booking-success/", views.booking_success, name="booking_success"),
    path("not-available/", views.not_available, name="not_available"),
    path("api/geocode/", views.geocode, name="geocode"),
    path("route/", views.route, name="route"),
    # Admin URLs
    # path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    # path("admin-bookings/", views.admin_bookings, name="admin_bookings"),
    # path(,
    #     "admin-booking-details/<int:booking_id>/",
    #     views.admin_booking_details,
    #     name="admin_booking_details",
    # ),
    # path("admin-new-booking/", views.admin_new_booking, name="admin_new_booking"),
    # path(
    #     "update-booking-status/<int:booking_id>/",
    #     views.update_booking_status,
    #     name="update_booking_status",
    # ),
    # path(
    #     "delete-booking/<int:booking_id>/", views.delete_booking, name="delete_booking"
    # ),
]
