import requests
import os
from dotenv import load_dotenv
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    city = input("Enter city name: ")
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Set your API key as an environment variable
    print(api_key)
    if not api_key:
        print("Please set the OPENWEATHER_API_KEY environment variable.")
    else:
        try:
            data = get_weather_data(city, api_key)
            print(f"Weather in {city}: {data['weather'][0]['description']}, Temperature: {data['main']['temp']}°C")
        except Exception as e:
            print(f"Error fetching weather data: {e}")