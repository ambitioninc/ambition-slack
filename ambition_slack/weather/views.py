# import json
import logging
import os

from django.http import HttpResponse
from django.views.generic.base import View

import slack

slack.weather_api_token = os.environ['SLACK_WEATHER_API_TOKEN']
LOG = logging.getLogger('console_logger')


class WeatherView(View):

    def get(self, *args, **kwargs):
        return HttpResponse('weather')

    def post(self, request, *args, **kwargs):

        # payload = json.loads(request.body)
        return HttpResponse()
