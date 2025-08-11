from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from .models import RoadSegment, TrafficReading


class TrafficReadingSerializer(serializers.ModelSerializer):
    @extend_schema_field(OpenApiTypes.STR)
    def get_intensity(self, obj):
        return obj.intensity

    intensity = serializers.SerializerMethodField()

    class Meta:
        model = TrafficReading
        fields = ['id', 'road_segment', 'average_speed', 'timestamp', 'intensity']


class RoadSegmentSerializer(GeoFeatureModelSerializer):
    readings_count = serializers.IntegerField(read_only=True)

    # Documenta o campo geom como GeoJSON no schema da API
    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_geom(self, obj):
        return obj.geom.geojson if obj.geom else None

    class Meta:
        model = RoadSegment
        geo_field = 'geom'
        fields = ['id', 'geom', 'length', 'speed', 'readings_count']
