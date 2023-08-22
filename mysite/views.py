from django.shortcuts import render, redirect
from django.http import request
import requests
import datetime

# Create your views here.

def index(request):
    api_key = open('API_KEY.txt', 'r').read()
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

    if request.method == 'POST':
        city = request.POST['city']
        try:
            weather_data = fetch_weather(city, api_key, current_weather_url)

            context = {
                'weather_data': weather_data,
            }

            return render(request, 'index.html', context)
        except KeyError:
            return render(request, 'key_error.html')
    else:
        return render(request, 'index.html')


def fetch_weather(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    return weather_data