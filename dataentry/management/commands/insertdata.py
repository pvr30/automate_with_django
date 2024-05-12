from django.core.management.base import BaseCommand
from dataentry.models import Student


class Command(BaseCommand):
    help = 'It will insert data to the database'

    def handle(self, *args, **kwargs):
        dataset = [
            {"roll_no": 1, "name": "Vishal", "age": 20},
            {"roll_no": 2, "name": "Harsh", "age": 21},
            {"roll_no": 3, "name": "Sanju", "age": 22}
        ]

        for data in dataset:
            existing_data = Student.objects.filter(roll_no=data['roll_no']).exists()
            if not existing_data:
                Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
                self.stdout.write(self.style.SUCCESS('Data inserted successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Already exists {data['roll_no']}'))

