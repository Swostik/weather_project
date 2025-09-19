import sqlite3
import pandas as pd

def get_cities_from_db(db_path='weather.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cities")
    cities = cursor.fetchall()
    conn.close()
    return cities

if __name__ == "__main__":
    cities = get_cities_from_db()
    df = pd.DataFrame(cities, columns=['index', 'cityname', 'lat', 'lon'])
    print(df)
    