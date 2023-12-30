import csv
import os
import requests

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{dir_path}/../../../phones.csv", "r") as file:
            phones = list(csv.DictReader(file, delimiter=";"))

        for phone in phones:
            response = requests.get(phone.get("image"), stream=True)
            image = ContentFile(response.content, name=f'{phone.get("name")}.jpg')
            Phone.objects.create(
                name=phone.get("name"),
                price=phone.get("price"),
                release_date=phone.get("release_date"),
                lte_exists=phone.get("lte_exists"),
                image=image,
            )
