from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomerForm
from .models import Bus, Customer
from django.contrib import messages
import datetime

# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class CheckAvailabilityView(View):
    def get(self, request):
        form = CustomerForm()
        return render(request, "check_availability.html", {"form": form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                # Simpan data customer ke database
                customer = Customer.objects.create(
                    name=form.cleaned_data["name"],
                    gender=form.cleaned_data["gender"],
                    phone=form.cleaned_data["phone"],
                )

                rental_date = form.cleaned_data["rental_date"]

                # Check if any bus is available on the selected date
                available_buses = []
                for bus_type in ["A", "B", "C"]:
                    buses = Bus.objects.filter(bus_type=bus_type)
                    for bus in buses:
                        if bus.is_available(rental_date, rental_date):
                            available_buses.append(bus_type)
                            break

                if not available_buses:
                    messages.error(
                        request, "Tidak ada bus yang tersedia pada tanggal yang dipilih"
                    )
                    return render(request, "not_available.html")

                # Store data in session for next step
                request.session["customer_id"] = customer.id
                request.session["rental_date"] = rental_date.isoformat()
                request.session["available_buses"] = available_buses

                messages.success(request, "Data berhasil disimpan")
                return redirect("select_bus_type")

            except Exception as e:
                messages.error(request, f"Terjadi kesalahan: {str(e)}")
                return render(request, "check_availability.html", {"form": form})

        # Jika form tidak valid
        messages.error(request, "Mohon periksa kembali input Anda")
        return render(request, "check_availability.html", {"form": form})


class SelectBusTypeView(View):
    def get(self, request):
        # Cek apakah ada data yang diperlukan di session
        if "customer_id" not in request.session or "rental_date" not in request.session:
            messages.error(request, "Silakan isi form pemesanan terlebih dahulu")
            return redirect("check_availability")

        rental_date = datetime.date.fromisoformat(request.session["rental_date"])

        # Hitung jumlah bus yang tersedia untuk setiap tipe
        available_counts = {"A": 0, "B": 0, "C": 0}
        total_counts = {"A": 14, "B": 7, "C": 4}  # Sesuai dengan jumlah bus yang ada

        for bus_type in available_counts.keys():
            buses = Bus.objects.filter(bus_type=bus_type)
            for bus in buses:
                if bus.is_available(rental_date, rental_date):
                    available_counts[bus_type] += 1

        return render(
            request,
            "select_bus_type.html",
            {
                "available_counts": available_counts,
                "total_counts": total_counts,
            },
        )

    def post(self, request):
        # Cek apakah ada data yang diperlukan di session
        if "customer_id" not in request.session or "rental_date" not in request.session:
            messages.error(request, "Silakan isi form pemesanan terlebih dahulu")
            return redirect("check_availability")

        bus_type = request.POST.get("bus_type")
        if bus_type not in ["A", "B", "C"]:
            messages.error(request, "Tipe bus tidak valid")
            return redirect("select_bus_type")

        # Simpan tipe bus yang dipilih ke session
        request.session["bus_type"] = bus_type
        return redirect("route_selection")
