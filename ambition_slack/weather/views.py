from django.http import HttpResponse
from django.views.generic.base import View

from ambition_slack.weather.lat_long_lookup import lat_long_lookup
from ambition_slack.weather.weather_summary import weather_summary


class WeatherView(View):

    def get(self, request, *args, **kwargs):
        location = request.GET['text']
        lat_long = lat_long_lookup(location)
        weather = weather_summary(lat_long)
        return HttpResponse(weather)
