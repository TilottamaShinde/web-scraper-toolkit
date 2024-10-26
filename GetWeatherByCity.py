import requests
from django.views.decorators.http import condition

from SimpleWeatherScraper import location_key


def get_location_key(api_key,city_name):
    #construct the search URL with the city name provided by the user

    search_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city_name}, India"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["Key"]
    print(f"Failed to get location key for {city_name}")
    return None

def get_weather_conditions(api_key, location_key, city_name):
    #Construct weather url with retrieved location url
    weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"
    response = requests.get(weather_url)

    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            temperature = data[0].get("Temperature",{}).get("Metric",{}).get("Value","N/A")
            condition = data[0].get("WeatherText","N/A")
            humidity = data[0].get("RelativeHumidity","N/A")
            wind_speed = data[0].get("Wind", {}).get("Speed",{}).get("Metric",{}).get("Value","N/A")

            print(f"Current Weather in {city_name}:")
            print(f"Temperature: {temperature} C")
            print(f"Condition: {condition}")
            print(f"Humidity: {humidity}")
            print(f"Wind speed: {wind_speed} km/hr")
        else:
            print("No weather data found")

    else:
        print("Failed to load weather data from AccuWeather API")
        # Replace with your AccuWeather API key
api_key = "Replace with your API Key"

#Prompt the user to to enter city name
city_name = input("Enter the name of Indian City : ")

#Get the location key for the user's city
location_key = get_location_key(api_key,city_name)

#If valid location is retrieved, get the current weather conditions
if location_key:
    get_weather_conditions(api_key, location_key, city_name)