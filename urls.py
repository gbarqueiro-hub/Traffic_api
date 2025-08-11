from django.urls import path, include

urlpatterns = [
    # outras urls
    path('api/', include('traffic_api.urls')),
]