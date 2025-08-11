import uuid
from django.utils import timezone
from django.contrib.gis.geos import LineString
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db import models  # usar GIS para campos geográficos


class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    location = models.PointField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class RoadSegment(models.Model):
    id = models.AutoField(primary_key=True)
    long_start = models.FloatField(null=True, blank=True)
    lat_start = models.FloatField(null=True, blank=True)
    long_end = models.FloatField(null=True, blank=True)
    lat_end = models.FloatField(null=True, blank=True)
    length = models.FloatField()
    speed = models.FloatField()
    geom = gis_models.LineStringField(srid=4326, null=True, blank=True)


    def __str__(self):
        return f"Segment {self.id}"

    def save(self, *args, **kwargs):
        # Atualiza o campo geom sempre que salvar o modelo
        self.geom = LineString(
            (self.long_start, self.lat_start),
            (self.long_end, self.lat_end),
            srid=4326
        )
        super().save(*args, **kwargs)

class Reading(models.Model):
    segment = models.ForeignKey(
        RoadSegment,
        related_name='readings',  # Importante para o serializer funcionar
        on_delete=models.CASCADE
    )
    speed = models.FloatField()
    # outros campos...



class TrafficReading(models.Model):
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, related_name='readings')
    average_speed = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Intensity:
        LOW = 'low'
        MEDIUM = 'medium'
        HIGH = 'high'
        CHOICES = [
            (HIGH, 'Elevada'),
            (MEDIUM, 'Média'),
            (LOW, 'Baixa'),
        ]

    @property
    def intensity(self):
        # Calcular intensidade de tráfego com base na velocidade média (regra do enunciado)
        if self.average_speed <= 20:
            return self.Intensity.HIGH
        elif 20 < self.average_speed <= 50:
            return self.Intensity.MEDIUM
        else:
            return self.Intensity.LOW

    def __str__(self):
        # Usar __str__ do RoadSegment
        return f"{self.road_segment} - {self.average_speed} km/h em {self.timestamp}"
    


    