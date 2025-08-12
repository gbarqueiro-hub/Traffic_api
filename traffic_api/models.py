import uuid
from django.utils import timezone
from django.contrib.gis.geos import LineString
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db import models  # usar GIS para campos geográficos
from django.contrib import admin


class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    location = gis_models.PointField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class RoadSegment(models.Model):
    id = models.AutoField(primary_key=True)
    long_start = models.FloatField(null=True, blank=True)
    lat_start = models.FloatField(null=True, blank=True)
    long_end = models.FloatField(null=True, blank=True)
    lat_end = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    geom = gis_models.LineStringField(srid=4326, null=True, blank=True)

    def __str__(self):
        return f"Segment {self.id}"

    def save(self, *args, **kwargs):
        # Corrigir geom: precisa ser uma lista/tupla de pontos
        if self.long_start is not None and self.lat_start is not None and \
           self.long_end is not None and self.lat_end is not None:
            self.geom = LineString([
                (self.long_start, self.lat_start),
                (self.long_end, self.lat_end)
            ], srid=4326)
        super().save(*args, **kwargs)

    @property
    def total_readings(self):
        return self.readings.count()

    @property
    def last_reading(self):
        return self.readings.order_by('-timestamp').first()

    @property
    def last_average_speed(self):
        last = self.last_reading
        return last.average_speed if last else None

    @property
    def last_intensity(self):
        last = self.last_reading
        return last.intensity if last else None



class Reading(models.Model):
    segment = models.ForeignKey(
        RoadSegment,
        related_name='sensor_readings',  # nome diferente aqui
        on_delete=models.CASCADE
    )
    speed = models.FloatField()
    # outros campos...



class TrafficReading(models.Model):
    road_segment = gis_models.ForeignKey(RoadSegment, on_delete=models.CASCADE, related_name='readings')
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
        if self.average_speed <= 20:
            return self.Intensity.HIGH
        elif 20 < self.average_speed <= 50:
            return self.Intensity.MEDIUM
        else:
            return self.Intensity.LOW

    def __str__(self):
        return f"{self.road_segment} - {self.average_speed} km/h em {self.timestamp}"


    