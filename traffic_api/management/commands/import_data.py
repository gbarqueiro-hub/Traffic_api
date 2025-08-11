import csv
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point, LineString
from traffic_api.models import RoadSegment, TrafficReading
from django.utils import timezone

class Command(BaseCommand):
    help = 'Importa sensores e leituras de arquivos CSV'

    def add_arguments(self, parser):
        parser.add_argument('--sensores', type=str, help='Caminho para o arquivo sensores.csv')
        parser.add_argument('--traffic_speed', type=str, help='Caminho para o arquivo traffic_speed.csv')

    def handle(self, *args, **options):
        sensores_path = options.get('sensores')
        traffic_speed_path = options.get('traffic_speed')

        if not sensores_path or not traffic_speed_path:
            self.stderr.write('É preciso passar os dois arquivos --sensores e --traffic_speed')
            return

        self.stdout.write('Importando sensores...')
        with open(sensores_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                RoadSegment.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'uuid': row['uuid']
                    }
                )
        self.stdout.write('Sensores importados.')

        self.stdout.write('Importando leituras e atualizando geometrias...')
        with open(traffic_speed_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                segment_id = int(row['ID'])
                start_point = Point(float(row['Long_start']), float(row['Lat_start']), srid=4326)
                end_point = Point(float(row['Long_end']), float(row['Lat_end']), srid=4326)
                line = LineString(start_point, end_point, srid=4326)
                speed = float(row['Speed'])

                # Atualiza a geometria do segmento
                RoadSegment.objects.filter(id=segment_id).update(geom=line)

                # Cria uma leitura nova, usando timestamp atual
                TrafficReading.objects.create(
                    road_segment_id=segment_id,
                    average_speed=speed,
                    timestamp=timezone.now()
                )
        self.stdout.write('Leituras importadas e geometrias atualizadas.')
 