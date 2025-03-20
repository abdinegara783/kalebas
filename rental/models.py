# models.py
from django.db import models
from django.utils import timezone
import datetime


class Bus(models.Model):
    BUS_TYPES = [
        ("A", "Type A"),
        ("B", "Type B"),
        ("C", "Type C"),
    ]

    name = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=1, choices=BUS_TYPES)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} (Type {self.bus_type})"

    def is_available(self, start_date, end_date):
        bookings = self.booking_set.filter(
            models.Q(start_date__lte=end_date, end_date__gte=start_date)
        )
        return not bookings.exists()

    @classmethod
    def get_least_busy_bus(cls, bus_type, start_date, end_date):
        buses = cls.objects.filter(bus_type=bus_type)

        # Calculate number of bookings in the next week for each bus
        now = timezone.now().date()
        week_later = now + datetime.timedelta(days=7)

        least_busy_bus = None
        min_bookings = float("inf")

        for bus in buses:
            if bus.is_available(start_date, end_date):
                bookings_count = bus.booking_set.filter(
                    start_date__gte=now, start_date__lte=week_later
                ).count()

                if bookings_count < min_bookings:
                    min_bookings = bookings_count
                    least_busy_bus = bus

        return least_busy_bus


class Customer(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# class Location(models.Model):
#     name = models.CharField(max_length=200)
#     latitude = models.FloatField()
#     longitude = models.FloatField()

#     def __str__(self):
#         return self.name


# class Booking(models.Model):
#     PAYMENT_STATUS = [
#         ("DP", "Down Payment"),
#         ("PAID", "Fully Paid"),
#         ("PENDING", "Pending"),
#     ]

#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     pickup_location = models.ForeignKey(
#         Location, on_delete=models.CASCADE, related_name="pickup_bookings"
#     )
#     destination = models.ForeignKey(
#         Location, on_delete=models.CASCADE, related_name="destination_bookings"
#     )
#     additional_locations = models.ManyToManyField(
#         Location, blank=True, related_name="additional_bookings"
#     )
#     total_distance = models.FloatField(help_text="Distance in kilometers")
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_status = models.CharField(
#         max_length=10, choices=PAYMENT_STATUS, default="PENDING"
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Booking {self.id} - {self.customer.name} - {self.bus.name}"

#     def calculate_price(self):
#         # Base rate per kilometer
#         rate_per_km = {
#             "A": 10000,  # Rp 10,000 per km for Type A
#             "B": 15000,  # Rp 15,000 per km for Type B
#             "C": 20000,  # Rp 20,000 per km for Type C
#         }

#         # Calculate number of days
#         days = (self.end_date - self.start_date).days + 1

#         # Calculate base price based on distance and bus type
#         base_price = self.total_distance * rate_per_km[self.bus.bus_type]

#         # Apply multiplier for number of days
#         total_price = base_price * days

#         return total_price
