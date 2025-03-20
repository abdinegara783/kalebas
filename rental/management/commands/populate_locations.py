from django.core.management.base import BaseCommand
from rental.models import Location

class Command(BaseCommand):
    help = "Populate database with initial location data"

    def handle(self, *args, **options):
        # Hapus data lokasi yang ada (optional)
        Location.objects.all().delete()

        # Data lokasi awal
        locations = [
            {
                "name": "Terminal Pulogadung",
                "address": "Jl. Perintis Kemerdekaan, Pulogadung, Jakarta Timur",
                "latitude": -6.1833,
                "longitude": 106.9000
            },
            {
                "name": "Terminal Kampung Rambutan",
                "address": "Jl. TB Simatupang, Ciracas, Jakarta Timur",
                "latitude": -6.3000,
                "longitude": 106.8833
            },
            # Tambahkan lokasi lain sesuai kebutuhan
        ]

        for loc_data in locations:
            Location.objects.create(**loc_data)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {Location.objects.count()} locations")
        )