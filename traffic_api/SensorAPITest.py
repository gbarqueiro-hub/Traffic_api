from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase, APIClient
from .models import Sensor

class SensorAPITest(APITestCase):
    def setUp(self):
        # Criar grupos
        self.manager_group = Group.objects.create(name='manager')

        # Usuários
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.manager_user = User.objects.create_user('manager', 'manager@test.com', 'password')
        self.manager_user.groups.add(self.manager_group)
        self.anonymous_client = APIClient()

        # Autenticados
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)

        self.manager_client = APIClient()
        self.manager_client.force_authenticate(user=self.manager_user)

        # Criar um sensor para testes
        self.sensor = Sensor.objects.create(name="Sensor 1", uuid="12345678-1234-5678-1234-567812345678")

    def test_list_sensors_anonymous(self):
        response = self.anonymous_client.get('/api/sensors/')
        self.assertEqual(response.status_code, 200)

    def test_create_sensor_admin(self):
        data = {
            "name": "Novo Sensor",
            "uuid": "87654321-4321-8765-4321-876543218765",
            "location": {"type": "Point", "coordinates": [10.0, 20.0]}
        }
        response = self.admin_client.post('/api/sensors/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_sensor_manager(self):
        data = {
            "name": "Sensor Manager",
            "uuid": "87654321-4321-8765-4321-876543218765",
            "location": {"type": "Point", "coordinates": [10.0, 20.0]}
        }
        response = self.manager_client.post('/api/sensors/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_delete_sensor_manager_forbidden(self):
        url = f'/api/sensors/{self.sensor.id}/'
        response = self.manager_client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_delete_sensor_admin(self):
        url = f'/api/sensors/{self.sensor.id}/'
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, 204)