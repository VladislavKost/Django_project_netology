from django.shortcuts import render, redirect
from django.urls import reverse
from csv import DictReader
from django.conf import settings
from django.core.paginator import Paginator


def index(request):
    return redirect(reverse("bus_stations"))


def bus_stations(request):
    page_number = int(request.GET.get("page", 1))
    stations = []
    with open(settings.BUS_STATION_CSV, newline="", encoding="utf-8") as csvfile:
        content = DictReader(csvfile)
        for row in content:
            name = row["Name"]
            street = row["Street"]
            district = row["District"]
            stations.append(
                {
                    "Name": name,
                    "Street": street,
                    "District": district,
                }
            )
    paginator = Paginator(stations, 10)
    page_content = paginator.get_page(page_number)
    context = {
        "bus_stations": page_content,
        "page": page_content,
    }
    return render(request, "stations/index.html", context)
