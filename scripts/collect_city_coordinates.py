import requests

# List of major European capital cities
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

if __name__ == "__main__":
    results = []
    for city in cities:
        coords = get_coordinates(city)
        print(f"{coords['city']}: Latitude={coords['latitude']}, Longitude={coords['longitude']}")
        results.append(coords)
    print(results)