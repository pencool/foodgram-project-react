import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Ingredient

path = Path(settings.BASE_DIR).resolve().parent.parent.joinpath(
    'data/ingredients.csv')


class Command(BaseCommand):
    help = 'Команда предназначена для импорта ингредиентов из CSV файла.'

    def handle(self, *args, **options):
        with open(path, 'r', encoding='utf-8') as f:
            for name, mes in csv.reader(f):
                Ingredient.objects.create(name=name, measurement_unit=mes)
                self.stdout.write(f'{name}=={self.style.SUCCESS("OK.")}')
            self.stdout.write(f'{self.style.SUCCESS("Импорт выполнен.")}')
