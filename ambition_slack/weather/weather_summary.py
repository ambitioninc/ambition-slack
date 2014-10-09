import forecastio
import os


def weather_summary(lat_long):
    latitude = lat_long[0]
    longitude = lat_long[1]
    api_key = os.environ['FORECASTIO_API_KEY']
    forecast = forecastio.load_forecast(api_key, latitude, longitude)
    byHour = forecast.hourly()
    message = byHour.summary
    return message
