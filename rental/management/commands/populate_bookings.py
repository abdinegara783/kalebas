from django.core.management.base import BaseCommand
from django.utils import timezone
from rental.models import Bus, Customer, Location, Booking
from datetime import timedelta, date
import random


class Command(BaseCommand):
    help = "Populate database with dummy booking data"

    def handle(self, *args, **options):
        # Check if we have buses, customers and locations
        if not Bus.objects.exists():
            self.stdout.write("Please run populate_buses first")
            return

        if not Location.objects.exists():
            self.stdout.write("Please run populate_locations first")
            return

        # Create some dummy customers if none exist
        if not Customer.objects.exists():
            self.create_dummy_customers()

        # Clear existing bookings
        Booking.objects.all().delete()

        # Get all available data
        buses = Bus.objects.all()
        customers = Customer.objects.all()
        locations = Location.objects.all()

        # Create bookings for the next 30 days
        today = timezone.now().date()

        for _ in range(50):  # Create 50 random bookings
            bus = random.choice(buses)
            customer = random.choice(customers)

            # Random start date between today and next 30 days
            start_date = today + timedelta(days=random.randint(0, 30))
            # Random duration between 1-7 days
            duration = random.randint(1, 7)
            end_date = start_date + timedelta(days=duration - 1)

            # Random locations
            pickup = random.choice(locations)
            while True:
                destination = random.choice(locations)
                if destination != pickup:
                    break

            # Random distance and calculate price
            distance = random.uniform(50, 500)  # 50-500 km
            base_rate = {"A": 10000, "B": 15000, "C": 20000}[bus.bus_type]
            total_price = distance * base_rate * duration

            # Check if bus is available for these dates
            if not Booking.objects.filter(
                bus=bus, start_date__lte=end_date, end_date__gte=start_date
            ).exists():
                # Create booking
                booking = Booking.objects.create(
                    customer=customer,
                    bus=bus,
                    start_date=start_date,
                    end_date=end_date,
                    pickup_location=pickup,
                    destination=destination,
                    total_distance=distance,
                    total_price=total_price,
                    payment_status=random.choice(["DP", "PAID", "PENDING"]),
                )

                # Add random additional locations
                additional_count = random.randint(0, 3)
                additional_locations = random.sample(
                    list(locations.exclude(id__in=[pickup.id, destination.id])),
                    min(additional_count, locations.count() - 2),
                )
                booking.additional_locations.add(*additional_locations)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {Booking.objects.count()} bookings"
            )
        )

    def create_dummy_customers(self):
        dummy_customers = [
            {"name": "John Doe", "gender": "M", "phone": "08123456789"},
            {"name": "Jane Smith", "gender": "F", "phone": "08234567890"},
            {"name": "Bob Johnson", "gender": "M", "phone": "08345678901"},
            {"name": "Alice Brown", "gender": "F", "phone": "08456789012"},
            {"name": "Charlie Wilson", "gender": "M", "phone": "08567890123"},
        ]

        for customer_data in dummy_customers:
            Customer.objects.create(**customer_data)

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(dummy_customers)} dummy customers")
        )
