from rest_framework.test import APITestCase
from django.urls import reverse
from traffic_api.models import RoadSegment

class RoadSegmentFilterTest(APITestCase):
    def setUp(self):
        self.segment1 = RoadSegment.objects.create(name="Main Street", long_start=0, lat_start=0, long_end=1, lat_end=1)
        self.segment2 = RoadSegment.objects.create(name="Second Ave", long_start=0, lat_start=0, long_end=2, lat_end=2)

    def test_filter_by_name(self):
        url = reverse('roadsegment-list')
        response = self.client.get(url, {'search': 'Main'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("Main" in seg['name'] for seg in response.data))
