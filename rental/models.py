from django.db import models
from datetime import timedelta


class Bus(models.Model):
    BUS_TYPES = [
        ("A", "Type A (40 passengers)"),
        ("B", "Type B (30 passengers)"),
        ("C", "Type C (20 passengers)"),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=BUS_TYPES)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} (Type {self.type})"


class Booking(models.Model):
    PAYMENT_STATUS = [
        ("PENDING", "Pending"),
        ("DP", "Down Payment"),
        ("PAID", "Paid"),
    ]

    # Customer information
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)

    # Bus and dates
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    start_date = models.DateField()
    rental_days = models.IntegerField(default=1)
    end_date = models.DateField()

    # Route information
    pickup = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    additional_locations = models.TextField(blank=True, null=True)  # Stored as JSON
    pickup_coordinates = models.CharField(max_length=50, blank=True)
    destination_coordinates = models.CharField(max_length=50, blank=True)
    total_distance = models.DecimalField(max_digits=10, decimal_places=2)

    # Price and payment
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS, default="PENDING"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate end date if not provided
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.rental_days - 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} - {self.customer_name} ({self.start_date})"

    def get_additional_locations_list(self):
        """Convert the JSON string to a list of locations"""
        import json

        if self.additional_locations:
            try:
                return json.loads(self.additional_locations)
            except:
                return []
        return []

    def set_additional_locations_list(self, locations_list):
        """Convert a list of locations to a JSON string"""
        import json

        if locations_list:
            self.additional_locations = json.dumps(locations_list)
        else:
            self.additional_locations = None

    def get_route_map_url(self):
        """Generate Google Maps URL for the route"""
        if self.pickup_coordinates and self.destination_coordinates:
            pickup_lat, pickup_lng = self.pickup_coordinates.split(",")
            dest_lat, dest_lng = self.destination_coordinates.split(",")
            return f"https://www.google.com/maps/dir/{pickup_lat},{pickup_lng}/{dest_lat},{dest_lng}"
        return None
