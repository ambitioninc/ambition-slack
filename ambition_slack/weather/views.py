import random
from django.http import HttpResponse
from django.views.generic.base import View
from ambition_slack.weather.lat_long_lookup import lat_long_lookup
from ambition_slack.weather.weather_summary import weather_summary


class WeatherView(View):

    def get(self, request, *args, **kwargs):
        location = request.GET['text']
        user = request.GET['user_name']
        answers = [
            'The answer lies in your heart',
            'I do not know',
            'You spelt weather wrong',
            'Nope',
            'Shh, I am trying to sleep',
            'Why do you need to ask?',
            'Go away. I do not wish to answer at this time.',
            'The window is 5 feet away. Stop being lazy', ]
        if user == 'jeff.mcriffey':
            weather = random.choice(answers)
        elif location == '':
            lat_long = lat_long_lookup('37403')
            weather = weather_summary(lat_long)
        else:
            lat_long = lat_long_lookup(location)
            weather = weather_summary(lat_long)
        return HttpResponse(weather)
