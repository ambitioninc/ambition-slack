from django.test import TestCase
from mock import patch


class WeatherViewUnitTest(TestCase):
    @patch('ambition_slack.weather.views.lat_long_lookup', spec_set=True)
    @patch('ambition_slack.weather.views.weather_summary', spec_set=True)
    def test_get_w_no_location(self, mock_weather_summary, mock_lat_long_lookup):
        """
        Tests the get method in the WeatherView when there is no location provided
        by the user.
        """
        self.client.get('/weather/?text=')
        mock_lat_long_lookup.assert_called_once_with('37403')
        mock_weather_summary.assert_called_once_with(mock_lat_long_lookup.return_value)

    @patch('ambition_slack.weather.views.lat_long_lookup', spec_set=True)
    @patch('ambition_slack.weather.views.weather_summary', spec_set=True)
    def test_get_w_location(self, mock_weather_summary, mock_lat_long_lookup):
        """
        Tests the get method in the WeatherView when there is a location provided
        by user.
        """
        self.client.get('/weather/?text=44444')
        mock_lat_long_lookup.assert_called_once_with('44444')
        mock_weather_summary.assert_called_once_with(mock_lat_long_lookup.return_value)

    @patch('ambition_slack.weather.weather_summary.forecastio')
    def test_return_value(self, forecastio):
        # Setup the scenario
        summary = 'It is raining dummy. Look out the window.'
        forecastio.load_forecast.return_value.hourly.return_value.summary = summary

        # Run the code
        response = self.client.get('/weather/?text=')

        # Verify expectation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(summary, response.content)
