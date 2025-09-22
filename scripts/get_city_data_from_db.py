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

if __name__ == "__main__":
    cities = get_cities_from_db()
    df = pd.DataFrame(cities, columns=['index', 'city', 'lat', 'lon'])
    print(df)
    