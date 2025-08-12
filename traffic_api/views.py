from rest_framework import viewsets, permissions,  generics, exceptions, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import RoadSegment, TrafficReading
from .serializers import RoadSegmentSerializer, TrafficReadingSerializer , Sensor , SensorSerializer  
from .permissions import CustomPermission
from .filters import RoadSegmentFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Car, Sensor, RoadSegment, Passage
from django.utils import timezone
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .serializers import PassageSerializer 

from rest_framework import generics

RoadSegment.objects.annotate(readings_count=Count('readings'))

queryset = RoadSegment.objects.annotate(readings_count=Count('readings'))

class RoadSegmentList(generics.ListAPIView):
    queryset = RoadSegment.objects.annotate(readings_count=Count('readings'))
    serializer_class = RoadSegmentSerializer

class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all().annotate(readings_count=Count('readings'))
    serializer_class = RoadSegmentSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter, drf_filters.SearchFilter]
    filterset_class = RoadSegmentFilter
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    permission_classes = [CustomPermission]

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_superuser:
            instance.delete()
        elif user.groups.filter(name='manager').exists():
            raise exceptions.PermissionDenied("Managers não têm permissão para deletar.")
        else:
            raise exceptions.PermissionDenied("Sem permissão para deletar.")



class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [CustomPermission]

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_superuser:
            instance.delete()
        elif user.groups.filter(name='manager').exists():
            raise exceptions.PermissionDenied("Managers não têm permissão para deletar sensores.")
        else:
            raise exceptions.PermissionDenied("Sem permissão para deletar sensores.")


class TrafficReadingViewSet(viewsets.ModelViewSet):
    """
    CRUD para leituras de velocidade média.
    Permissões:
    - supermanager: create, read, update, delete
    - manager: create, read, update, sem delete
    - anônimo: read apenas
    """
    queryset = TrafficReading.objects.all().order_by('-timestamp')
    serializer_class = TrafficReadingSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter, drf_filters.SearchFilter]
    filterset_fields = ['road_segment', 'timestamp']
    ordering_fields = ['timestamp', 'average_speed']
    search_fields = []


    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_superuser:
            instance.delete()
        elif user.groups.filter(name='manager').exists():
            raise exceptions.PermissionDenied("Managers não têm permissão para deletar.")
        else:
            raise exceptions.PermissionDenied("Sem permissão para deletar.")




API_KEY = "23231c7a-80a7-4810-93b3-98a18ecfbc42"

class HasValidAPIKey(BasePermission):
    def has_permission(self, request, view):
        key = request.headers.get("X-API-KEY")
        return key == API_KEY

class SensorBulkPassageUploadView(APIView):
    permission_classes = [HasValidAPIKey]

    def post(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Esperado uma lista de passagens"}, status=status.HTTP_400_BAD_REQUEST)

        created = 0
        errors = []

        for idx, entry in enumerate(data):
            try:
                road_segment_id = entry.get("road_segment")
                license_plate = entry.get("car__license_plate")
                timestamp_str = entry.get("timestamp")
                sensor_uuid = entry.get("sensor__uuid")

                if not (road_segment_id and license_plate and timestamp_str and sensor_uuid):
                    raise ValueError("Campos obrigatórios em falta")

                road_segment = RoadSegment.objects.get(pk=road_segment_id)
                sensor = Sensor.objects.get(uuid=sensor_uuid)
                car, _ = Car.objects.get_or_create(license_plate=license_plate, defaults={'registered_at': timezone.now()})

                timestamp = timezone.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                Passage.objects.create(
                    road_segment=road_segment,
                    car=car,
                    sensor=sensor,
                    timestamp=timestamp
                )
                created += 1
            except Exception as e:
                errors.append({"index": idx, "error": str(e)})

        if errors:
            return Response({"created": created, "errors": errors}, status=status.HTTP_207_MULTI_STATUS)
        return Response({"created": created}, status=status.HTTP_201_CREATED)






class CarPassagesLast24hView(generics.ListAPIView):
    serializer_class = PassageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        license_plate = self.request.query_params.get('license_plate')
        if not license_plate:
            return Passage.objects.none()  # ou lançar erro custom

        car = get_object_or_404(Car, license_plate=license_plate)
        last_24h = timezone.now() - timezone.timedelta(hours=24)
        return Passage.objects.filter(car=car, timestamp__gte=last_24h).select_related('sensor', 'road_segment').order_by('-timestamp')