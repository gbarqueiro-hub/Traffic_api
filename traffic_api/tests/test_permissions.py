from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from rest_framework import status

class PermissionsTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', '1234')
        self.manager_group = Group.objects.create(name='manager')
        self.manager = User.objects.create_user('manager', 'manager@test.com', '1234')
        self.manager.groups.add(self.manager_group)
        self.user = User.objects.create_user('user', 'user@test.com', '1234')

    def test_admin_can_write(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/alguma-url/', {})
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_write_but_not_delete(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/alguma-url/', {})
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/alguma-url/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_write(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/alguma-url/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_can_only_read(self):
        response = self.client.get('/alguma-url/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/alguma-url/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
