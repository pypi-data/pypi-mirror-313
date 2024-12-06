import requests
from typing import Optional
from unidecode import unidecode


def get_department(city_name: str) -> Optional[str]:
    """
    Get department for a given city from OpenDataSoft API.

    Args:
        city_name (str): Name of the city.

    Returns:
        Optional[str]: Name of the department for the given city, or None if not found.
    """
    base_url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-france-commune/records"
    params = {
        "select": "com_name_lower,dep_name",
        "where": f"com_name_lower = '{unidecode(city_name.strip().lower())}'",
        "limit": 1,
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data["results"]:
            department_name = data["results"][0]["dep_name"][0]
            return department_name
        print(f"No department found for city {city_name}.")
        return None
    print(f"Error fetching data: {response.status_code}")
    return None
