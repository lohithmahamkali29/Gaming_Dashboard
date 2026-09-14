from django.test import TestCase
from rest_framework.test import APIClient

from devices.models import Rig
from .models import Race, RaceEntry


class RaceTelemetryTests(TestCase):
    def setUp(self):
        self.rig = Rig.objects.create(name='Telemetry Rig', provider='mock')
        self.race = Race.objects.create(name='Test Race', total_laps=3, status='ready')
        RaceEntry.objects.create(race=self.race, rig=self.rig, driver_name='Driver One')

    def test_start_and_telemetry_endpoints(self):
        client = APIClient()
        self.assertEqual(client.post(f'/api/races/{self.race.pk}/start/').status_code, 200)
        response = client.get(f'/api/races/{self.race.pk}/telemetry/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'running')
        self.assertIn('speed', response.json()['entries'][0]['telemetry'])
