import logging

from django.http import HttpResponse
from django.views.generic.base import View

from ambition_slack.weather.weather_summary import weather_summary
LOG = logging.getLogger('console_logger')

LATITUDE = 35.046772
LONGITUDE = -85.308863


class WeatherView(View):

    def get(self, request, *args, **kwargs):
        weather = weather_summary(LATITUDE, LONGITUDE)
        return HttpResponse(weather)
