from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
import json
import random
import calendar

from .models import Bus, Booking
from .forms import BookingForm, AdminBookingForm


# Customer-facing views
def home(request):
    return render(request, "home.html")


def booking_page(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Get form data
            customer_name = form.cleaned_data["name"]
            customer_phone = form.cleaned_data["phone"]
            bus_type = form.cleaned_data["bus_type"]
            rental_date = form.cleaned_data["rental_date"]
            rental_days = form.cleaned_data["rental_days"]
            pickup = form.cleaned_data["pickup"]
            destination = form.cleaned_data["destination"]
            end_date = rental_date + timedelta(days=rental_days - 1)

            # Process additional locations
            additional_locations = []
            if form.cleaned_data["additional_locations"]:
                additional_locations = json.loads(
                    form.cleaned_data["additional_locations"]
                )

            # Get all buses of the selected type
            buses = Bus.objects.filter(type=bus_type)

            # Find available bus
            available_bus = None
            for bus in buses:
                # Check if bus is booked during the requested period
                conflicting_bookings = Booking.objects.filter(
                    bus=bus, start_date__lte=end_date, end_date__gte=rental_date
                )

                if not conflicting_bookings.exists():
                    available_bus = bus
                    break

            # If no bus is available, redirect to not_available page
            if not available_bus:
                return redirect("not_available")

            # Calculate distance (simplified)
            distance = random.randint(50, 500)  # Random distance between 50-500 km

            # Calculate price
            rate_per_km = {
                "A": 10000,  # Rp 10,000 per km for Type A
                "B": 15000,  # Rp 15,000 per km for Type B
                "C": 20000,  # Rp 20,000 per km for Type C
            }

            base_price = distance * rate_per_km[bus_type]
            total_price = base_price * rental_days

            # Create booking
            booking = Booking(
                customer_name=customer_name,
                customer_phone=customer_phone,
                bus=available_bus,
                start_date=rental_date,
                end_date=end_date,
                rental_days=rental_days,
                pickup=pickup,
                destination=destination,
                additional_locations=json.dumps(additional_locations)
                if additional_locations
                else None,
                total_distance=distance,
                total_price=total_price,
                payment_status="PENDING",
            )
            booking.save()

            # Redirect to booking confirmation
            return redirect("booking_confirmation", booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, "booking.html", {"form": form})


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        # Update booking with calculated distance
        calculated_distance = float(request.POST.get("calculated_distance", 0))
        booking.total_distance = calculated_distance

        # Recalculate price based on new distance
        rate_per_km = {
            "A": 10000,  # Rp 10,000 per km for Type A
            "B": 15000,  # Rp 15,000 per km for Type B
            "C": 20000,  # Rp 20,000 per km for Type C
        }
        booking.total_price = calculated_distance * rate_per_km[booking.bus.type]

        booking.save()
        return redirect("booking_success")

    return render(request, "booking_confirmation.html", {"booking": booking})


def booking_success(request):
    return render(request, "booking_success.html")


def not_available(request):
    return render(request, "not_available.html")


# # Admin views
# @login_required
# def admin_dashboard(request):
#     # Get month and year from query parameters or use current date
#     now = timezone.now()
#     month = int(request.GET.get("month", now.month))
#     year = int(request.GET.get("year", now.year))

#     # Get all buses
#     buses = Bus.objects.all().order_by("type", "name")

#     # Get days in month
#     days_in_month = calendar.monthrange(year, month)[1]
#     days = list(range(1, days_in_month + 1))

#     # Get all bookings for the month
#     start_of_month = datetime(year, month, 1).date()
#     end_of_month = datetime(year, month, days_in_month).date()

#     bookings = Booking.objects.filter(
#         Q(start_date__lte=end_of_month, end_date__gte=start_of_month)
#     )

#     # Create calendar data
#     calendar_data = {}

#     for bus in buses:
#         calendar_data[bus.id] = {}
#         for day in days:
#             calendar_data[bus.id][day] = None

#     # Fill in booking data
#     for booking in bookings:
#         start_day = (
#             max(booking.start_date.day, 1)
#             if booking.start_date.month == month and booking.start_date.year == year
#             else 1
#         )
#         end_day = (
#             min(booking.end_date.day, days_in_month)
#             if booking.end_date.month == month and booking.end_date.year == year
#             else days_in_month
#         )

#         for day in range(start_day, end_day + 1):
#             calendar_data[booking.bus.id][day] = {
#                 "id": booking.id,
#                 "customer_name": booking.customer_name,
#                 "start_date": booking.start_date,
#                 "end_date": booking.end_date,
#                 "payment_status": booking.payment_status,
#             }

#     context = {
#         "buses": buses,
#         "days": days,
#         "bookings": calendar_data,
#         "month": month,
#         "year": year,
#         "month_name": calendar.month_name[month],
#     }

#     return render(request, "bus_rental/admin/dashboard.html", context)


# @login_required
# def admin_bookings(request):
#     status = request.GET.get("status")

#     if status:
#         bookings = Booking.objects.filter(payment_status=status).order_by("-created_at")
#     else:
#         bookings = Booking.objects.all().order_by("-created_at")

#     context = {
#         "bookings": bookings,
#         "status": status,
#     }

#     return render(request, "bus_rental/admin/bookings.html", context)


# @login_required
# def admin_booking_details(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)

#     if request.method == "POST":
#         action = request.POST.get("action")

#         if action == "update_status":
#             status = request.POST.get("status")
#             if status in dict(Booking.PAYMENT_STATUS).keys():
#                 booking.payment_status = status
#                 booking.save()
#                 messages.success(
#                     request,
#                     f"Booking status updated to {dict(Booking.PAYMENT_STATUS)[status]}",
#                 )

#         elif action == "delete":
#             booking.delete()
#             messages.success(request, "Booking deleted successfully")
#             return redirect("admin_bookings")

#     return render(
#         request, "bus_rental/admin/booking_details.html", {"booking": booking}
#     )


# @login_required
# def admin_new_booking(request):
#     if request.method == "POST":
#         form = AdminBookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)

#             # Calculate distance (simplified)
#             distance = random.randint(50, 500)  # Random distance between 50-500 km

#             # Calculate price
#             rate_per_km = {
#                 "A": 10000,  # Rp 10,000 per km for Type A
#                 "B": 15000,  # Rp 15,000 per km for Type B
#                 "C": 20000,  # Rp 20,000 per km for Type C
#             }

#             base_price = distance * rate_per_km[booking.bus.type]
#             total_price = base_price * booking.rental_days

#             booking.total_distance = distance
#             booking.total_price = total_price
#             booking.save()

#             messages.success(request, "Booking created successfully")
#             return redirect("admin_booking_details", booking_id=booking.id)
#     else:
#         form = AdminBookingForm()

#     return render(request, "bus_rental/admin/new_booking.html", {"form": form})


# @login_required
# def update_booking_status(request, booking_id):
#     if request.method == "POST":
#         booking = get_object_or_404(Booking, id=booking_id)
#         status = request.POST.get("status")

#         if status in dict(Booking.PAYMENT_STATUS).keys():
#             booking.payment_status = status
#             booking.save()
#             messages.success(
#                 request, f"Status updated to {dict(Booking.PAYMENT_STATUS)[status]}"
#             )

#     return redirect("admin_booking_details", booking_id=booking_id)


# @login_required
# def delete_booking(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     booking.delete()
#     messages.success(request, "Booking deleted successfully")
#     return redirect("admin_bookings")

from django.shortcuts import render
from django.http import JsonResponse
import requests
import json


def route(request):
    """
    View for the main route finder page
    """
    return render(request, "route.html")


def geocode(request):
    """
    API view to proxy geocoding requests to Nominatim
    """
    query = request.GET.get("query", "")

    if not query:
        return JsonResponse({"error": "Query parameter is required"}, status=400)

    try:
        # Forward the request to Nominatim with Indonesia country code
        response = requests.get(
            f"https://nominatim.openstreetmap.org/search",
            params={"format": "json", "q": query, "countrycodes": "id", "limit": 5},
            headers={
                "User-Agent": "RouteFinderApp/1.0 Django",
                "Accept-Language": "en",
            },
        )

        if response.status_code != 200:
            return JsonResponse(
                {"error": f"Nominatim API error: {response.status_code}"}, status=500
            )

        data = response.json()
        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse(
            {"error": f"Failed to fetch location data: {str(e)}"}, status=500
        )
