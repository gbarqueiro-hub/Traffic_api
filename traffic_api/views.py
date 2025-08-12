from rest_framework import viewsets, permissions, exceptions, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import RoadSegment, TrafficReading
from .serializers import RoadSegmentSerializer, TrafficReadingSerializer , Sensor , SensorSerializer  
from .permissions import CustomPermission
from .filters import RoadSegmentFilter


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
