from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Reading, RoadSegment

@receiver([post_save, post_delete], sender=Reading)
def update_segment_speed(sender, instance, **kwargs):
    segment = instance.segment
    readings = segment.readings.all()
    if readings.exists():
        avg_speed = readings.aggregate(Avg('speed'))['speed__avg']
        segment.speed = avg_speed
    else:
        segment.speed = None
    segment.save()
