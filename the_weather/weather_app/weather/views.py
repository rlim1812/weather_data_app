import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    # specify API endpoint
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=2fc015141be19a16d51d1a2814946403"

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        city_name = city.name
        # make a GET request to the API
        response = requests.get(url.format(city_name)).json()

        # extract relevant data out of json object
        city_weather = {
            "city": city_name,
            "temperature": response["main"]["temp"],
            "description": response["weather"][0]["description"],
            "icon": response["weather"][0]["icon"]
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)
