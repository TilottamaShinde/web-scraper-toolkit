import requests


def get_location_key(api_key):

    search_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q=Pune"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["Key"]  # Retrieve the first result's location key
    print("Failed to get location key for Pune.")
    return None


def get_weather_conditions(api_key, location_key):
    weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"
    response = requests.get(weather_url)

    if response.status_code == 200:
        data = response.json()
        print("Weather data response:", data)
        if len(data) > 0:
            temperature = data[0].get("Temperature", {}).get("Metric", {}).get("Value", "N/A")
            condition = data[0].get("WeatherText", "N/A")
            humidity = data[0].get("RelativeHumidity", "N/A")  # Use get() to avoid KeyError
            wind_speed = data[0].get("Wind", {}).get("Speed", {}).get("Metric", {}).get("Value", "N/A")

            print(f"Current Weather in Pune:")
            print(f"Temperature: {temperature} °C")
            print(f"Condition: {condition}")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} km/h")
        else:
            print("No weather data found")
    else:
        print("Failed to retrieve weather data from AccuWeather API.")


# Replace with your AccuWeather API key
api_key = "ACCUWEATHER_API_KEY"

# Get the location key for Pune
location_key = get_location_key(api_key)

# If a valid location key is retrieved, get the current weather conditions
if location_key:
    get_weather_conditions(api_key, location_key)

