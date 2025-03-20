# urls.py
from django.urls import path
from .views import (
    HomeView,
    CheckAvailabilityView,
    SelectBusTypeView,
    # RouteSelectionView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "check-availability/",
        CheckAvailabilityView.as_view(),
        name="check_availability",
    ),
    path("select-bus-type/", SelectBusTypeView.as_view(), name="select_bus_type"),
    # path("route-selection/", RouteSelectionView.as_view(), name="route_selection"),
]
