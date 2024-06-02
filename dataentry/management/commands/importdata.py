import csv
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import DataError


class Command(BaseCommand):
    help = 'Import data from csv file.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='to get file path')
        parser.add_argument('model_name', type=str, help='Model name to pass')

    def handle(self, *args, **kwargs):
        file_path = kwargs.get('file_path')
        model_name = kwargs.get('model_name').capitalize()

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue

        if not model:
            raise CommandError(f"Model {model_name} not found.")

        model_fields = [field.name for field in model._meta.fields if field.name != 'id']

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            if csv_header != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields.")

            for row in reader:
                model.objects.get_or_create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from csv successfully.'))
