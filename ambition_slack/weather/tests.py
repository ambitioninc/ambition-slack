from django.test import TestCase
from mock import patch

from ambition_slack.weather.lat_long_lookup import lat_long_lookup


class WeatherViewUnitTest(TestCase):
    @patch('ambition_slack.weather.views.lat_long_lookup', spec_set=True)
    @patch('ambition_slack.weather.views.weather_summary', spec_set=True)
    def test_get_w_no_location(self, mock_weather_summary, mock_lat_long_lookup):
        """
        Tests the get method in the WeatherView when there is no location provided
        by the user.
        """
        self.client.get('/weather/?user_name=batman&text=')
        mock_lat_long_lookup.assert_called_once_with('37403')
        mock_weather_summary.assert_called_once_with(mock_lat_long_lookup.return_value)

    @patch('ambition_slack.weather.views.lat_long_lookup', spec_set=True)
    @patch('ambition_slack.weather.views.weather_summary', spec_set=True)
    def test_get_w_location(self, mock_weather_summary, mock_lat_long_lookup):
        # Run the code
        self.client.get('/weather/?user_name=batman&text=Dallas')

        # Verify expectation
        mock_lat_long_lookup.assert_called_once_with('Dallas')
        mock_weather_summary.assert_called_once_with(mock_lat_long_lookup.return_value)

    @patch('ambition_slack.weather.views.random.choice', spec_set=True)
    def test_get_user_name(self, choice):
        answer = 'Random message'
        choice.return_value = answer
        # Run the code
        response = self.client.get('/weather/?user_name=jeff.mcriffey&text=Dallas')

        # Verify expectation
        self.assertEqual(answer, response.content)

    @patch('ambition_slack.weather.lat_long_lookup.requests')
    def test_weather_view_lat_long(self, requests):
        # Setup scenario
        payload = {'results': [{'geometry': {'location': {'lat': 35.0357569, 'lng': -85.3197919}}}]}
        latitude = 35.0357569
        longitude = -85.3197919
        requests.get.return_value.json.return_value = payload
        # Verify expectation
        self.assertEqual(lat_long_lookup(37403), (latitude, longitude))

    @patch('ambition_slack.weather.weather_summary.forecastio')
    def test_return_value(self, forecastio):
        # Setup the scenario
        summary = 'It is raining dummy. Look out the window.'
        forecastio.load_forecast.return_value.hourly.return_value.summary = summary

        # Run the code
        response = self.client.get('/weather/?user_name=batman&text=')

        # Verify expectation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(summary, response.content)
