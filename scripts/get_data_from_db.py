import sqlite3
import pandas as pd

def get_cities_from_db(db_path='weather.db') -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cities")
    cities = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(cities, columns=['index', 'city_name', 'lat', 'lon'])
    return df

def get_most_recent_date_from_weather(db_path='weather.db') -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date) FROM weather_data")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] else None

if __name__ == "__main__":
    cities = get_cities_from_db()
    df = pd.DataFrame(cities, columns=['index', 'city', 'lat', 'lon'])
    print(df)
    