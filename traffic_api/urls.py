from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RoadSegmentViewSet, TrafficReadingViewSet

router = DefaultRouter()
router.register(r'roadsegments', RoadSegmentViewSet, basename='roadsegment')
router.register(r'trafficreadings', TrafficReadingViewSet, basename='trafficreading')

urlpatterns = [
    path('', include(router.urls)),
]
