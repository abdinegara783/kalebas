from django.core.management.base import BaseCommand
from rental.models import Bus, Booking
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = "Create dummy bookings for testing"

    def handle(self, *args, **options):
        # Tanggal dimana semua bus akan dipesan (25 April 2025)
        fully_booked_date = date(2025, 4, 25)

        # Hapus booking yang ada
        Booking.objects.all().delete()

        # Buat booking untuk semua bus pada tanggal yang ditentukan
        buses = Bus.objects.all()
        for bus in buses:
            Booking.objects.create(
                customer_name=f"Test Customer {bus.name}",
                customer_phone="08123456789",
                bus=bus,
                start_date=fully_booked_date,
                rental_days=2,  # 2 hari rental
                end_date=fully_booked_date + timedelta(days=1),
                pickup="Jakarta",
                destination="Bandung",
                total_distance=150,
                total_price=2000000,
                payment_status="PAID",
            )

        # Buat beberapa booking acak untuk tanggal lain di April 2025
        for _ in range(10):
            random_bus = random.choice(buses)
            random_start_date = date(2025, 4, random.randint(1, 30))

            # Skip jika tanggal sama dengan fully_booked_date
            if random_start_date == fully_booked_date:
                continue

            rental_days = random.randint(1, 3)

            Booking.objects.create(
                customer_name=f"Random Customer {_}",
                customer_phone="08123456789",
                bus=random_bus,
                start_date=random_start_date,
                rental_days=rental_days,
                end_date=random_start_date + timedelta(days=rental_days - 1),
                pickup="Jakarta",
                destination="Bandung",
                total_distance=random.randint(100, 300),
                total_price=random.randint(1000000, 3000000),
                payment_status=random.choice(["PENDING", "DP", "PAID"]),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created dummy bookings. All buses are booked on {fully_booked_date}"
            )
        )
