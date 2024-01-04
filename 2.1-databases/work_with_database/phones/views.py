from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect("catalog")


def show_catalog(request):
    template = "catalog.html"
    SORT_MAP = {
        "name": "name",
        "min_price": "price",
        "max_price": "-price",
    }
    filter_value = request.GET.get("sort", "name")
    phone_objects = Phone.objects.order_by(SORT_MAP.get(filter_value))
    context = {"phones": phone_objects}
    return render(request, template, context)


def show_product(request, slug):
    template = "product.html"
    phones = Phone.objects.filter(slug=slug)[:1]
    context = {}
    for phone in phones:
        context = {
            "phone": {
                "name": phone.name,
                "price": phone.price,
                "image": phone.image,
                "slug": phone.slug,
                "release_date": phone.release_date,
            }
        }
    return render(request, template, context)
