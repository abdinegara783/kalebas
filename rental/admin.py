from django.contrib import admin
from .models import Bus, Booking


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "capacity")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "bus",
        "start_date",
        "end_date",
        "payment_status",
    )
    list_filter = ("payment_status", "start_date")
    search_fields = ("customer_name", "customer_phone")
    date_hierarchy = "start_date"
