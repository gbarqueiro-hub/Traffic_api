from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from .models import RoadSegment, TrafficReading



class RoadSegmentSerializer(GeoFeatureModelSerializer):
    readings_count = serializers.SerializerMethodField()
    intensity = serializers.SerializerMethodField()

    class Meta:
        model = RoadSegment
        geo_field = 'geom'
        fields = ['id', 'geom', 'length', 'speed', 'readings_count', 'intensity']

    def get_readings_count(self, obj):
        return obj.readings.count()

    def get_intensity(self, obj):
        # Usar intensidade da última leitura, se existir
        last_intensity = obj.last_intensity
        if last_intensity is None:
            return "Desconhecida"
        # Traduzir valores para exibir
        mapping = {
            'low': "Baixa",
            'medium': "Média",
            'high': "Elevada"
        }
        return mapping.get(last_intensity, "Desconhecida")


class TrafficReadingSerializer(serializers.ModelSerializer):
    intensity = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_intensity(self, obj):
        mapping = {
            'low': "Baixa",
            'medium': "Média",
            'high': "Elevada"
        }
        return mapping.get(obj.intensity, "Desconhecida")

    def get_description(self, obj):
        # Usa o __str__ do modelo para uma descrição amigável
        return str(obj)

    class Meta:
        model = TrafficReading
        fields = ['id', 'road_segment', 'average_speed', 'timestamp', 'intensity', 'description']