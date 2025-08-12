from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import BasePermission
from django.utils import timezone
from traffic_api.models import Car, Sensor, RoadSegment, Passage

API_KEY = "23231c7a-80a7-4810-93b3-98a18ecfbc42"

class HasValidAPIKey(BasePermission):
    def has_permission(self, request, view):
        key = request.headers.get("X-API-KEY")
        return key == API_KEY

class PassageBulkUploadSerializer(serializers.Serializer):
    road_segment = serializers.IntegerField()
    car_license_plate = serializers.CharField(max_length=20)
    timestamp = serializers.DateTimeField()
    sensor_uuid = serializers.UUIDField()

class SensorBulkPassageUploadView(APIView):
    permission_classes = [HasValidAPIKey]
    serializer_class = PassageBulkUploadSerializer  # <-- aqui

    def post(self, request, *args, **kwargs):
        # Validação via serializer (muitos registros)
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        created = 0
        errors = []

        for idx, entry in enumerate(serializer.validated_data):
            try:
                road_segment = RoadSegment.objects.get(pk=entry["road_segment"])
                sensor = Sensor.objects.get(uuid=entry["sensor_uuid"])
                car, _ = Car.objects.get_or_create(
                    license_plate=entry["car_license_plate"], 
                    defaults={'registered_at': timezone.now()}
                )
                Passage.objects.create(
                    road_segment=road_segment,
                    car=car,
                    sensor=sensor,
                    timestamp=entry["timestamp"]
                )
                created += 1
            except Exception as e:
                errors.append({"index": idx, "error": str(e)})

        if errors:
            return Response({"created": created, "errors": errors}, status=status.HTTP_207_MULTI_STATUS)
        return Response({"created": created}, status=status.HTTP_201_CREATED)
