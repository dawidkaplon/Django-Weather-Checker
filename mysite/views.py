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
            return render(request, 'index.html', {'error': 'There is no such city!'})
    else:
        return render(request, 'index.html')


def fetch_weather(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    description = response['weather'][0]['description']

    if 'clear' in description:
        icon_src = 'https://i.ibb.co/TrJ8RhK/sun.png'
    elif 'clouds' in description:
        icon_src = 'https://i.ibb.co/C1QZ55c/clouds.png'
    elif 'rain' in description:
        icon_src = 'https://i.ibb.co/MV8VFLv/rain.png'
    elif 'thunderstorm' in description:
        icon_src = 'https://i.ibb.co/h7rp53z/thunderstorm.png'
    elif 'snow' in description:
        icon_src = 'https://i.ibb.co/rc5mHb1/snow.png'
    elif 'mist' in description:
        icon_src = 'https://i.ibb.co/wwFBTfS/mist.png'
        
    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 1),
        'description': description,
        'icon': icon_src,
        'country': response['sys']['country'],
        'feel_temp': round(response['main']['feels_like'] - 273.15, 1),
        'min_temp': round(response['main']['temp_min'] - 273.15, 1),
        'max_temp': round(response['main']['temp_max'] - 273.15, 1),
        'wind_speed': response['wind']['speed'],
        'pressure': response['main']['pressure'],
        'humidity': response['main']['humidity'],
    }

    return weather_data