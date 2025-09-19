import requests
import os
from dotenv import load_dotenv

from get_city_data_from_db import get_cities_from_db
import pandas as pd
import sqlite3
import time

def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    df_cities_with_lat_lon = get_cities_from_db()
    print(df_cities_with_lat_lon)
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Please set the OPENWEATHER_API_KEY environment variable.")
    else:
        weather_data = []
        for idx, row in df_cities_with_lat_lon.iterrows():
            city = row['city']
            lat = row['lat']
            lon = row['lon']
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                weather_desc = data['weather'][0]['description']
                timestamp = pd.Timestamp.now()
                temp = data['main']['temp']
            except Exception as e:
                weather_desc = None
                temp = None
            
            weather_data.append({'weather_description': weather_desc, 'temperature': temp, 'date': timestamp})

        weather_df = pd.DataFrame(weather_data)
        df_cities_with_lat_lon = pd.concat([df_cities_with_lat_lon.reset_index(drop=True), weather_df], axis=1)
        print(df_cities_with_lat_lon)
conn = sqlite3.connect('/Users/swostikshrestha/Documents/Swostik/weather_project/weather.db')
df_cities_with_lat_lon.to_sql('weather_data', conn, if_exists='replace', index=False)
conn.close()