import csv
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.apps import apps


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

        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file_path = f'exported_{model_name}_{timestamp}.csv'

        with open(file_path, 'w', newline='') as file:
            objs = model.objects.all()

            writer = csv.writer(file)
            writer.writerow([field.name for field in model._meta.fields])
            for obj in objs:
                writer.writerow([getattr(obj, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported to csv successfully.'))
