from rest_framework.test import APITestCase
from django.urls import reverse
from traffic_api.models import RoadSegment, Sensor
from django.utils import timezone
import uuid

class BulkPassageUploadTest(APITestCase):
    def setUp(self):
        self.road_segment = RoadSegment.objects.create(long_start=0, lat_start=0, long_end=1, lat_end=1)
        self.sensor = Sensor.objects.create(name="Sensor 1", uuid=str(uuid.uuid4()))
        self.url = reverse('sensor-bulk-passage-upload')
        self.api_key = "23231c7a-80a7-4810-93b3-98a18ecfbc42"

    def test_bulk_upload(self):
        payload = [{
            "road_segment": self.road_segment.id,
            "car__license_plate": "TEST123",
            "timestamp": timezone.now().isoformat(),
            "sensor__uuid": self.sensor.uuid
        }]
        response = self.client.post(self.url, payload, format='json', HTTP_X_API_KEY=self.api_key)
        self.assertEqual(response.status_code, 201)
