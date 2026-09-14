from django.test import TestCase
from rest_framework.test import APIClient

from .models import Rig


class DeviceApiTests(TestCase):
    def test_health_endpoint(self):
        response = APIClient().get('/api/devices/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_rig_api_creates_rig(self):
        response = APIClient().post('/api/devices/rigs/', {'name': 'Test Rig'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Rig.objects.filter(name='Test Rig').exists())
