from rest_framework.test import APITestCase
from django.urls import reverse
from traffic_api.models import Sensor

class SensorViewSetTest(APITestCase):
    def test_list_sensors(self):
        Sensor.objects.create(name="S1", uuid="uuid-1234")
        url = reverse('sensor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
