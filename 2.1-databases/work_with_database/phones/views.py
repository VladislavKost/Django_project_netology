from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect("catalog")


def show_catalog(request):
    template = "catalog.html"
    filter_value = request.GET.get("sort", "name")
    if filter_value == "min_price":
        filter_phones = "price"
    elif filter_value == "max_price":
        filter_phones = "-price"
    else:
        filter_phones = "name"
    phone_objects = Phone.objects.order_by(filter_phones)
    phones = []
    for phone in phone_objects:
        phones.append(
            {
                "name": phone.name,
                "price": phone.price,
                "image": phone.image,
                "slug": phone.slug,
            }
        )
    context = {"phones": phones}
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
