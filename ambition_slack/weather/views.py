import logging

from django.http import HttpResponse
from django.views.generic.base import View

from ambition_slack.weather.weather_summary import weather_summary
LOG = logging.getLogger('console_logger')

latitude = 35.046772
longitude = -85.308863


class WeatherView(View):

    def get(self, request, *args, **kwargs):
        weather = weather_summary(latitude, longitude)
        return HttpResponse(weather)
