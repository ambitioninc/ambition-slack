import forecastio
import os

def weather_summary(latitude, longitude):
	api_key = os.environ['FORECASTIO_API_KEY']
	forecast = forecastio.load_forecast(api_key, latitude, longitude)
	byHour = forecast.hourly()
	message = byHour.summary
	return message
