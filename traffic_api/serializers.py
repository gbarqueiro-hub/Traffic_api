from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from .models import RoadSegment, TrafficReading


class RoadSegmentSerializer(GeoFeatureModelSerializer):
    readings_count = serializers.IntegerField(read_only=True)
    intensity = serializers.SerializerMethodField()

    class Meta:
        model = RoadSegment
        geo_field = 'geom'
        fields = ['id', 'geom', 'length', 'speed', 'readings_count', 'intensity']

    def get_intensity(self, obj):
        if obj.speed is None:
            return "Desconhecida"
        if obj.speed > 50:
            return "Baixa"
        elif 30 <= obj.speed <= 50:
            return "Média"
        else:
            return "Elevada"

class TrafficReadingSerializer(serializers.ModelSerializer):
    @extend_schema_field(OpenApiTypes.STR)
    def get_intensity(self, obj):
        return obj.intensity

    intensity = serializers.SerializerMethodField()

    class Meta:
        model = TrafficReading
        fields = ['id', 'road_segment', 'average_speed', 'timestamp', 'intensity']


