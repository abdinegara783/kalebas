# # rental/admin.py
from django.contrib import admin
from .models import Bus, Customer, Location, Booking
# from django.utils.html import format_html
# from datetime import datetime, timedelta
# import calendar


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("name", "bus_type", "capacity")
    list_filter = ("bus_type",)
    search_fields = ("name",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "phone")
    list_filter = ("gender",)
    search_fields = ("name", "phone")

    # Optional: Tambahkan fieldsets untuk organisasi form yang lebih baik
    fieldsets = (
        ("Personal Information", {"fields": ("name", "gender")}),
        ("Contact Details", {"fields": ("phone",)}),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "latitude", "longitude")
    search_fields = ("name", "address")
    list_filter = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "bus",
        "start_date",
        "end_date",
        "payment_status",
        "total_price",
        "created_at",
    )
    list_filter = ("payment_status", "bus__bus_type", "start_date", "created_at")
    search_fields = (
        "customer__name",
        "bus__name",
        "pickup_location__name",
        "destination__name",
    )
    raw_id_fields = ("customer", "bus", "pickup_location", "destination")
    date_hierarchy = "start_date"

    fieldsets = (
        ("Customer and Bus", {"fields": ("customer", "bus")}),
        (
            "Booking Details",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "pickup_location",
                    "destination",
                    "additional_locations",
                )
            },
        ),
        (
            "Payment Information",
            {"fields": ("total_distance", "total_price", "payment_status")},
        ),
    )
