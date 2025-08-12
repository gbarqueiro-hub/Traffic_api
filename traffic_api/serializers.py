from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from .models import Passage, Car, RoadSegment, TrafficReading , Sensor



class RoadSegmentSerializer(GeoFeatureModelSerializer):
    readings_count = serializers.SerializerMethodField()
    intensity = serializers.SerializerMethodField()

    class Meta:
        model = RoadSegment
        geo_field = 'geom'
        fields = ['id', 'geom', 'length', 'speed', 'readings_count', 'intensity']

    @extend_schema_field(OpenApiTypes.INT)
    def get_readings_count(self, obj):
        # Usa o valor anotado na query para evitar queries extras
        return getattr(obj, 'readings_count', 0)

    @extend_schema_field(OpenApiTypes.STR)
    def get_intensity(self, obj):
        if obj.speed is None:
            return "Desconhecida"
        if obj.speed > 50:
            return "Baixa"
        elif 20 < obj.speed <= 50:
            return "Média"
        else:
            return "Elevada"



class SensorSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Sensor
        geo_field = "location"  # campo geográfico PointField
        fields = ['id', 'name', 'uuid', 'location']

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





class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'license_plate', 'registered_at']

class PassageSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    sensor = serializers.StringRelatedField()
    road_segment = serializers.StringRelatedField()

    class Meta:
        model = Passage
        fields = ['id', 'car', 'sensor', 'road_segment', 'timestamp']
