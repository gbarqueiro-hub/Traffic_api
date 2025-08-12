from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from traffic_api.views_bulk_upload import SensorBulkPassageUploadView
from traffic_api.views import CarPassagesLast24hView  


urlpatterns = [
    path('admin/', admin.site.urls),

    # Endpoints da API
    path('api/', include('traffic_api.urls')),

    # Schema e documentação
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Endpoints de bulk upload e consultas específicas
    path('passages/bulk_upload/', SensorBulkPassageUploadView.as_view(), name='bulk_upload'),
    path('api/passages/car/', CarPassagesLast24hView.as_view(), name='car_passages_last24h'),

]
