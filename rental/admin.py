# # rental/admin.py
from django.contrib import admin
from .models import Bus, Customer
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


# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "customer_name",
#         "bus",
#         "start_date",
#         "end_date",
#         "payment_status",
#         "booking_date",
#     )
#     list_filter = ("payment_status", "bus__tipe", "start_date")
#     search_fields = ("customer_name", "customer_phone", "bus__nama")
#     raw_id_fields = ("bus",)
#     date_hierarchy = "start_date"

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         form.base_fields["start_date"].widget.attrs["type"] = "date"
#         form.base_fields["end_date"].widget.attrs["type"] = "date"
#         return form
