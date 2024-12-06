import requests
from unidecode import unidecode
from typing import Dict, Optional


def get_coordinates(city_name: str, openweathermap_api_key: str) -> Optional[Dict[str, float]]:
    """
    Get coordinates for a given city from OpenWeatherMap API.

    Args:
        city_name (str): Name of the city.
        openweathermap_api_key (str): OpenWeatherMap API key.

    Returns:
        Optional[Dict[str, float]]: Dictionary with "lat" and "lon" keys, or None if not found.
    """
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{unidecode(city_name.strip().lower())}",
        "limit": 1,
        "appid": openweathermap_api_key
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        country_code = data[0]["country"] if data else None

        if not country_code:
            print(f"Country code not found for city {city_name}.")
            return None

        if country_code == "FR":
            city_coordinates = {"lat": data[0]["lat"], "lon": data[0]["lon"]}
            return city_coordinates
        print(f"City {city_name} not found in France. Please, specify a city known in France.")
        return None
    print(f"Error fetching data: {response.status_code}")
    return None
