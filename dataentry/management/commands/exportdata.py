import csv
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from dataentry.utils import generate_csv_file


class Command(BaseCommand):
    help = 'Export data from model to csv.'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Model name to pass')

    def handle(self, *args, **kwargs):
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

        file_path = generate_csv_file(model_name)

        with open(file_path, 'w', newline='') as file:
            objs = model.objects.all()

            writer = csv.writer(file)
            writer.writerow([field.name for field in model._meta.fields])
            for obj in objs:
                writer.writerow([getattr(obj, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported to csv successfully.'))
