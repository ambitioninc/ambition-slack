import forecastio
import logging
import slack
import os
# import json
from django.http import HttpResponse
from django.views.generic.base import View

api_key = os.environ['FORECASTIO_API_KEY']

slack.weather_api_token = os.environ['SLACK_WEATHER_API_TOKEN']
LOG = logging.getLogger('console_logger')


class WeatherView(View):

    def get(self, *args, **kwargs):
        return HttpResponse('weather')

    def post(self, request, *args, **kwargs):
    	lat = 35.046772
		lng = -85.308863

		forecast = forecastio.load_forecast(api_key, lat, lng)
		byHour = forecast.hourly()
		byHour.summary

        # payload = json.loads(request.body)
        return HttpResponse()
