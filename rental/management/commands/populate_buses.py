from django.core.management.base import BaseCommand
from rental.models import Bus


class Command(BaseCommand):
    help = "Populate database with initial bus data"

    def handle(self, *args, **options):
        # Hapus data bus yang ada (optional)
        Bus.objects.all().delete()

        # Buat bus tipe A (14 bus)
        for i in range(1, 15):
            Bus.objects.create(name=f"A-{i}", bus_type="A", capacity=52)

        # Buat bus tipe B (7 bus)
        for i in range(1, 8):
            Bus.objects.create(name=f"B-{i}", bus_type="B", capacity=30)

        # Buat bus tipe C (4 bus)
        for i in range(1, 5):
            Bus.objects.create(name=f"C-{i}", bus_type="C", capacity=21)

        self.stdout.write(self.style.SUCCESS("Successfully created 25 buses"))
