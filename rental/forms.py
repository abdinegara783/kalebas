from django import forms
from django.core.exceptions import ValidationError
from .models import Booking, Bus
import json
from datetime import datetime, timedelta


class BookingForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    bus_type = forms.ChoiceField(
        label="Bus Type",
        choices=[
            ("A", "Type A (40 passengers)"),
            ("B", "Type B (30 passengers)"),
            ("C", "Type C (20 passengers)"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    rental_date = forms.DateField(
        label="Rental Date",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    rental_days = forms.IntegerField(
        label="Number of Days",
        min_value=1,
        max_value=7,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    pickup = forms.CharField(
        label="Pickup Location",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    destination = forms.CharField(
        label="Destination",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    additional_locations_text = forms.CharField(
        label="Additional Locations (one per line)",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )

    def clean_rental_date(self):
        rental_date = self.cleaned_data.get("rental_date")
        if rental_date < datetime.now().date():
            raise ValidationError("Rental date cannot be in the past")
        return rental_date

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) < 10:
            raise ValidationError("Phone number must be at least 10 digits")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        # Get the additional locations from the POST data
        additional_locations = self.data.getlist("additional_locations[]")
        # Filter out empty values
        additional_locations = [
            loc.strip() for loc in additional_locations if loc.strip()
        ]
        cleaned_data["additional_locations"] = additional_locations
        return cleaned_data


class AdminBookingForm(forms.ModelForm):
    additional_locations_text = forms.CharField(
        label="Additional Locations (one per line)",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    class Meta:
        model = Booking
        fields = [
            "customer_name",
            "customer_phone",
            "bus",
            "start_date",
            "rental_days",
            "pickup",
            "destination",
            "payment_status",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter buses by type if provided in initial data
        if kwargs.get("initial") and "bus_type" in kwargs["initial"]:
            bus_type = kwargs["initial"]["bus_type"]
            self.fields["bus"].queryset = Bus.objects.filter(type=bus_type)

        # Set initial value for additional_locations_text
        if self.instance.pk and self.instance.additional_locations:
            try:
                locations = json.loads(self.instance.additional_locations)
                self.initial["additional_locations_text"] = "\n".join(locations)
            except:
                pass

    def clean(self):
        cleaned_data = super().clean()

        # Process additional locations
        additional_locations_text = cleaned_data.get("additional_locations_text", "")
        if additional_locations_text:
            locations = [
                loc.strip()
                for loc in additional_locations_text.split("\n")
                if loc.strip()
            ]
            cleaned_data["additional_locations"] = json.dumps(locations)
        else:
            cleaned_data["additional_locations"] = None

        # Calculate end date
        start_date = cleaned_data.get("start_date")
        rental_days = cleaned_data.get("rental_days", 1)
        if start_date:
            cleaned_data["end_date"] = start_date + timedelta(days=rental_days - 1)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set additional locations
        if "additional_locations" in self.cleaned_data:
            instance.additional_locations = self.cleaned_data["additional_locations"]

        # Calculate end date
        instance.end_date = instance.start_date + timedelta(
            days=instance.rental_days - 1
        )

        if commit:
            instance.save()
        return instance
