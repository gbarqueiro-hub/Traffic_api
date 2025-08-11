# traffic_api/filters.py
from django.db.models import OuterRef, Subquery, FloatField, Case, When, Value, CharField
from django_filters import rest_framework as filters
from .models import RoadSegment, TrafficReading

class RoadSegmentFilter(filters.FilterSet):
    """
    Filtra RoadSegment pela caracterização (elevada/média/baixa) da última leitura.
    Uso: /api/roadsegments/?intensity=elevada  (aceita 'elevada','media','média','baixa')
    """
    intensity = filters.CharFilter(method='filter_by_last_intensity')

    class Meta:
        model = RoadSegment
        fields = ['intensity']

    def filter_by_last_intensity(self, queryset, name, value):
        # Mapear termos PT -> valores internos ('high','medium','low')
        mapping = {
            'elevada': 'high',
            'media': 'medium',
            'média': 'medium',
            'baixa': 'low',
            'high': 'high',
            'medium': 'medium',
            'low': 'low',
        }
        v = (value or '').strip().lower()
        mapped = mapping.get(v)
        if not mapped:
            return queryset.none()

        # Subquery para obter a velocidade média mais recente por segmento
        last_speed_sq = Subquery(
            TrafficReading.objects.filter(road_segment=OuterRef('pk'))
            .order_by('-timestamp')
            .values('average_speed')[:1],
            output_field=FloatField()
        )

        # Anotar intensidade baseada na last_speed
        annotated = queryset.annotate(last_speed=last_speed_sq).annotate(
            last_intensity=Case(
                When(last_speed__lte=20, then=Value('high')),
                When(last_speed__lte=50, then=Value('medium')),
                default=Value('low'),
                output_field=CharField()
            )
        )
        return annotated.filter(last_intensity=mapped)
