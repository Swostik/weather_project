import sqlite3
from collect_city_coordinates import get_coordinates
from sqlalchemy import create_engine

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
    "Sofia, Bulgaria"
]

def insert_city(db_path, city_name, latitude, longitude):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cities (name, latitude, longitude)
        VALUES (?, ?, ?)
    ''', (city_name, latitude, longitude))
    conn.commit()
    conn.close()
    print(f"Inserted city: {city_name} ({latitude}, {longitude})")

def insert_weather_from_df(db_path, df):
    """
    Inserts weather data from a pandas DataFrame into the weather table.
    The DataFrame should have columns: city_name, temperature, humidity, weather_description, timestamp
    """

    conn = sqlite3.connect(db_path)
    df.to_sql('weather_data', conn, if_exists='replace', index=False)
    conn.close()
    

    print(f"Inserted {len(df)} weather records from DataFrame")

if __name__ == "__main__":
    # do not run 
    pass