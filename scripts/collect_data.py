import requests
import os
from dotenv import load_dotenv
import pandas as pd
import sqlite3
import time
import json

from get_city_data_from_db import get_cities_from_db
from insert_to_db import insert_weather_from_df, insert_city
from create_db import create_city_table

cities = [
    "London, United Kingdom",
    "Paris, France",
    "Berlin, Germany",
    "Madrid, Spain",
    "Rome, Italy",
    "Vienna, Austria",
    "Brussels, Belgium",
    "Amsterdam, Netherlands",
    "Copenhagen, Denmark",
    "Oslo, Norway",
    "Stockholm, Sweden",
    "Helsinki, Finland",
    "Dublin, Ireland",
    "Lisbon, Portugal",
    "Warsaw, Poland",
    "Prague, Czech Republic",
    "Budapest, Hungary",
    "Athens, Greece",
    "Bern, Switzerland",
    "Sofia, Bulgaria"]

def get_coordinates(city):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "city-coordinates-script"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        return {
            "city": city,
            "latitude": data[0]["lat"],
            "longitude": data[0]["lon"]
        }
    else:
        return {
            "city": city,
            "latitude": None,
            "longitude": None
        }

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
    # Check if the 'cities' table exists, else create it
    create_city_table()
   
    df_cities_with_lat_lon = get_cities_from_db()
    missing_cities = [city for city in cities if city not in df_cities_with_lat_lon['city_name'].values]
    if missing_cities:
        print("Missing cities in DataFrame:", missing_cities)
        # Find coordinates for missing cities and append to DataFrame
        new_city_coords = []
        for city in missing_cities:
            coords = get_coordinates(city)
            new_city_coords.append({
                'city_name': coords['city'],
                'lat': coords['latitude'],
                'lon': coords['longitude']
            })
        if new_city_coords:
            new_cities_df = pd.DataFrame(new_city_coords)
            # Save new cities with coordinates to the database
            for _, row in new_cities_df.iterrows():
                insert_city('weather.db', row['city_name'], row['lat'], row['lon'])
            df_cities_with_lat_lon = pd.concat([df_cities_with_lat_lon, new_cities_df], ignore_index=True)
    else:
        print("All cities are present in the DataFrame.")
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
            time.sleep(0.4) 
            print(len(weather_data)) # To respect API rate limits
        weather_df = pd.DataFrame(weather_data)
        print(weather_df)
        print(df_cities_with_lat_lon)
        df_cities_with_lat_lon = pd.concat([df_cities_with_lat_lon.reset_index(drop=True), weather_df], axis=1)
        print(df_cities_with_lat_lon)

        # Insert into database
        insert_weather_from_df('weather.db', df_cities_with_lat_lon)