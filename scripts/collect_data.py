import requests
import os
from dotenv import load_dotenv

from get_city_data_from_db import get_cities_from_db
import pandas as pd
import sqlite3
import time
import json

def get_weather_data(lat,lon, api_key):
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
    return {'latitude': lat, 'longitude': lon, 'weather_description': weather_desc, 'temperature': temp, 'date': timestamp}
    
def get_air_pollution_data(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pollution = data['list'][0]['main']['aqi']  # Air Quality Index (1-5)
        components = data['list'][0]['components']  # Pollutant concentrations
        timestamp = pd.Timestamp.now()
    except Exception as e:
        pollution = None
        components = None
        timestamp = pd.Timestamp.now()
    return {'aqi': pollution, 'components': components, 'date': timestamp}
    
if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    df_cities_with_lat_lon = get_cities_from_db()
    print(df_cities_with_lat_lon)
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Please set the OPENWEATHER_API_KEY environment variable.")
    else:
        weather_data = []
        for index, row in df_cities_with_lat_lon.iterrows():
            
            lat = row['lat']
            lon = row['lon']
            weather_info = get_weather_data(lat, lon, api_key)
            air_pollution_info = get_air_pollution_data(lat, lon, api_key)
            # Convert 'components' dict to JSON string for SQLite compatibility
            if air_pollution_info['components'] is not None:
                # Flatten the components dict into separate columns
                for comp_key, comp_value in air_pollution_info['components'].items():
                    air_pollution_info[f'component_{comp_key}'] = comp_value
                del air_pollution_info['components']
            combined_info = {**weather_info, **air_pollution_info}
            weather_data.append(combined_info)
            time.sleep(0.4)  # To respect API rate limits
        weather_df = pd.DataFrame(weather_data)
        df_cities_with_lat_lon = pd.concat([df_cities_with_lat_lon.reset_index(drop=True), weather_df], axis=1)
        print(df_cities_with_lat_lon)
conn = sqlite3.connect('/Users/swostikshrestha/Documents/Swostik/weather_project/weather.db')
df_cities_with_lat_lon.to_sql('weather_data', conn, if_exists='replace', index=False)
conn.close()