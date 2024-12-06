import requests
import pandas as pd
from typing import Optional

from energy_manager.apis.weather.get_coordinates import get_coordinates


def get_hourly_weather(city_name: str, openweathermap_api_key: str, timestamp: int) -> Optional[pd.DataFrame]:
   """
   Fetches weather data for a given city at a specific Unix timestamp from OpenWeatherMap API.

   Args:
       city_name (str): Name of the city.
       openweathermap_api_key (str): OpenWeatherMap API key.
       timestamp (int): Unix timestamp for the weather data.

   Returns:
       Optional[pd.DataFrame]: DataFrame with weather data, or None if data fetch fails.
   """
   base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine?"

   city_coordinates = get_coordinates(city_name=city_name, openweathermap_api_key=openweathermap_api_key)
   if not city_coordinates: return None

   params = {
      "lon": city_coordinates["lon"],
      "lat": city_coordinates["lat"],
      "dt": str(timestamp),
      "appid": openweathermap_api_key,
      "units": "metric",
   }
   response = requests.get(base_url, params=params)

   if response.status_code != 200:
      print(f"Error fetching weather data: {response.status_code}")
      return None

   data = response.json()

   required_columns = ["dt", "temp", "weather"]
   df_hourly_weather = pd.DataFrame(data["data"])[required_columns]
   df_hourly_weather["dt"] = pd.to_datetime(df_hourly_weather["dt"], unit="s")
   df_hourly_weather["weather"] = df_hourly_weather["weather"].apply(lambda x: x[0]["description"])
   df_hourly_weather["temp"] = df_hourly_weather["temp"].astype(float)

   df_hourly_weather.rename(columns={"dt": "date_time", "temp": "temperature", "weather": "weather_description"}, inplace=True)

   return df_hourly_weather
