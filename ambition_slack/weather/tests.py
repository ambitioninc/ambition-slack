from django.test import TestCase
from django.test.client import Client


class TestWeatherView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_weather_view(self):
        response = self.client.get('/weather/')
        self.assertEqual(response.status_code, 200)
