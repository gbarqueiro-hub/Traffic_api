from rest_framework.test import APITestCase
from traffic_api.models import RoadSegment, Reading

class SignalUpdateTest(APITestCase):
    def test_average_speed_updates(self):
        segment = RoadSegment.objects.create(long_start=0, lat_start=0, long_end=1, lat_end=1)
        Reading.objects.create(segment=segment, speed=50)
        Reading.objects.create(segment=segment, speed=70)
        segment.refresh_from_db()
        self.assertEqual(segment.speed, 60)
