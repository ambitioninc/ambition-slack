from django.test import TestCase
from django.test.client import Client
from mock import patch


class TestWeatherView(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('ambition_slack.weather.weather_summary.forecastio')
    def test_weather_view(self, forecastio):
        # Setup the scenario
        summary = 'It is raining'
        forecastio.load_forecast.return_value.hourly.return_value.summary = summary

        # Run the code
        response = self.client.get('/weather/')

        # Verify expectation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(summary, response.content)
