import csv
import uuid
from django.core.management.base import BaseCommand
from traffic_api.models import Sensor

class Command(BaseCommand):
    help = 'Importa sensores do CSV'

    def handle(self, *args, **kwargs):
        with open('data/sensors.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Sensor.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    uuid=uuid.UUID(row['uuid']),
                )
        self.stdout.write(self.style.SUCCESS('Sensores importados com sucesso!'))
