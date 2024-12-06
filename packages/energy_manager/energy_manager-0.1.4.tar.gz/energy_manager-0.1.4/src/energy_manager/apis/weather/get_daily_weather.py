import pandas as pd
from typing import List, Optional

from energy_manager.apis.weather.get_hourly_weather import *


def get_daily_weather(city_name: str, openweathermap_api_key: str, timestamps: List[int]) -> Optional[pd.DataFrame]:
   """
   Fetches weather data for a given city at some specified Unix timestamps.

   Args:
       city_name (str): Name of the city.
       openweathermap_api_key (str): OpenWeatherMap API key.
       timestamps (List[int]): List of Unix timestamps to fetch weather data for.

   Returns:
       Optional[pd.DataFrame]: Concatenated DataFrame with weather data, or None if all fetches fail.
   """
   if not get_coordinates(city_name=city_name, openweathermap_api_key=openweathermap_api_key): return None

   df_daily_weather = []
   for timestamp in timestamps:
      df_hourly_weather = get_hourly_weather(
         city_name=city_name,
         openweathermap_api_key=openweathermap_api_key,
         timestamp=timestamp
      )
      if df_hourly_weather is None:
         print(f"Failed to fetch weather data for timestamp {timestamp}.")
         return None
      df_daily_weather.append(df_hourly_weather)

   return pd.concat(df_daily_weather, ignore_index=True)
