import sqlite3
from collect_city_coordinates import get_coordinates

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

if __name__ == "__main__":
    # Example usage
    db_path = "weather.db"
    # Insert some dummy data into the cities table
    
    for city in cities:
        coords = get_coordinates(city)
        latitude = float(coords['latitude']) if coords['latitude'] else None
        longitude = float(coords['longitude']) if coords['longitude'] else None
        #print(f"{coords['city']}: Latitude={coords['latitude']}, Longitude={coords['longitude']}")
        insert_city(db_path, city, latitude, longitude)