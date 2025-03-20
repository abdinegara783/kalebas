# # forms.py
from django import forms
from .models import Customer


class CustomerForm(forms.Form):
    name = forms.CharField(max_length=100)
    gender = forms.ChoiceField(choices=[("M", "Male"), ("F", "Female")])
    phone = forms.CharField(max_length=15)
    rental_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))


# class LocationForm(forms.Form):
#     pickup = forms.CharField(max_length=200, label="Pickup Location")
#     destination = forms.CharField(max_length=200, label="Destination")
#     additional_locations = forms.CharField(
#         max_length=500,
#         required=False,
#         widget=forms.Textarea(attrs={"rows": 3}),
#         help_text="Enter additional locations, one per line (optional)",
#     )
#     rental_days = forms.IntegerField(
#         min_value=1, max_value=7, initial=1, label="Number of days to rent"
#     )

#     def clean_additional_locations(self):
#         data = self.cleaned_data["additional_locations"]
#         if data:
#             return [
#                 location.strip() for location in data.split("\n") if location.strip()
#             ]
#         return []
