import forecastio
import os

api_key = os.environ['FORECASTIO_API_KEY']
lat = 35.046772
lng = -85.308863

forecast = forecastio.load_forecast(api_key, lat, lng)
byHour = forecast.hourly()
byHour.summary
