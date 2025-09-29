import sqlite3



# Create a table to store city name, latitude, and longitude
def create_city_table(db_path='weather.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":

    
    create_city_table()
    