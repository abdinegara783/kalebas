from django.core.management.base import BaseCommand
from rental.models import Bus


class Command(BaseCommand):
    help = "Populate database with initial bus data"

    def handle(self, *args, **options):
        # Hapus data bus yang ada (optional)
        Bus.objects.all().delete()

        # Buat bus tipe A (14 bus)
        for i in range(1, 15):
            Bus.objects.create(
                name=f"A-{i}",
                type="A",  # Changed from bus_type to type
                capacity=52,
            )

        # Buat bus tipe B (7 bus)
        for i in range(1, 8):
            Bus.objects.create(
                name=f"B-{i}",
                type="B",  # Changed from bus_type to type
                capacity=30,
            )

        # Buat bus tipe C (4 bus)
        for i in range(1, 5):
            Bus.objects.create(
                name=f"C-{i}",
                type="C",  # Changed from bus_type to type
                capacity=21,
            )

        self.stdout.write(self.style.SUCCESS("Successfully created 25 buses"))
