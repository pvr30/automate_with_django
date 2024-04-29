from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Greeting Message'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='to parse argument')

    def handle(self, *args, **options):
        name = options.get('name')
        greet_msg = f'Hi {name}, Good Morning'
        self.stdout.write(self.style.WARNING(greet_msg))
