import sqlite3


def delete_latest_data(db_path: str, table_name: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE date = (SELECT MAX(date) FROM {table_name})")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    delete_latest_data('weather.db', 'weather_data')