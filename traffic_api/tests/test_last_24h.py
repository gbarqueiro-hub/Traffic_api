from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from traffic_api.models import Car, Passage, RoadSegment, Sensor

class CarPassagesLast24hViewTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', '1234')
        self.client.force_authenticate(user=self.admin)

        self.car = Car.objects.create(license_plate='TEST123')
        self.sensor = Sensor.objects.create(name='sensor', uuid='uuid-1')
        self.segment = RoadSegment.objects.create(long_start=0, lat_start=0, long_end=1, lat_end=1)

        Passage.objects.create(car=self.car, sensor=self.sensor, road_segment=self.segment, timestamp=timezone.now())

    def test_get_passages_last_24h(self):
        url = reverse('car_passages_last24h')
        response = self.client.get(url, {'license_plate': 'TEST123'})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
