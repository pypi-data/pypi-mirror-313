import gc
import numpy as np
import pandas as pd
from typing import Optional

from energy_manager.utils.set_edf_prices import set_edf_prices
from energy_manager.utils.set_hchp_hours import set_hchp_hours
from energy_manager.apis.weather.get_daily_weather import get_daily_weather
from energy_manager.utils.generate_daily_timestamps import generate_daily_timestamps
from energy_manager.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp
from energy_manager.apis.buildings.get_buildings_consumptions import get_buildings_consumptions


def compute_daily_expenses(
    user_city_name: str,
    openweathermap_api_key: str,
    user_temperature: float,
    user_dpe_usage: float,
    user_insulation_factor: Optional[float] = 1.0
) -> Optional[pd.DataFrame]:
    """
    Calculate expenses based on user input and city data.

    Args:
        user_city_name (str): Name of the user's city.
        openweathermap_api_key (str): OpenWeatherMap API key.
        user_temperature (float): Desired temperature by the user.
        user_dpe_usage (float): User's DPE usage.
        user_insulation_factor (float, optional): User's insulation factor. Defaults to 1.0.

    Returns:
        Optional[pd.DataFrame]: DataFrame with calculated expenses or None if data is not found.
    """
    df_buildings_consumptions = get_buildings_consumptions(city_name=user_city_name)

    if df_buildings_consumptions is None:
        print(f"No buildings consumption data found for the city {user_city_name}.")
        return None

    midnight_utc_timestamp = get_midnight_utc_timestamp()
    daily_timestamps = generate_daily_timestamps(start_timestamp=midnight_utc_timestamp)

    df_daily_weather = get_daily_weather(
        city_name=user_city_name,
        openweathermap_api_key=openweathermap_api_key,
        timestamps=daily_timestamps
    )
    df_daily_weather["degree_diff"] = np.abs(df_daily_weather["temperature"] - user_temperature)

    del df_daily_weather["temperature"], daily_timestamps, midnight_utc_timestamp
    gc.collect()

    df_hchp_hours = set_hchp_hours()
    df_merged = df_daily_weather.copy(deep=True)
    df_merged[df_hchp_hours.columns.tolist()[1:]] = df_hchp_hours[df_hchp_hours.columns.tolist()[1:]].copy(deep=True)

    df_edf_prices = set_edf_prices()
    df_merged_two = df_merged.copy(deep=True)
    df_merged_two["option_0"] = np.unique(
        df_edf_prices.loc[df_edf_prices["subscription"] == "Base", df_edf_prices.columns[1:]].values[0]
    )[0]

    other_options = ["option_1", "option_2", "option_3", "option_4"]
    df_merged_two[other_options] = df_merged_two[other_options].map(
        lambda hour_type: (
            df_edf_prices.loc[
                df_edf_prices["subscription"] == "Heures Creuses - Heures Pleines", "kwh_price_normal_hour"
            ].values[0] if hour_type == "HC"
            else df_edf_prices.loc[
                df_edf_prices["subscription"] == "Heures Creuses - Heures Pleines", "kwh_price_peak_hour"
            ].values[0]
        )
    )
    gc.collect()

    df_merged_three = df_merged_two.copy(deep=True)
    all_options = ["option_0"] + other_options
    df_merged_three[all_options] = df_merged_three[all_options].apply(
        lambda option_col: user_dpe_usage * option_col * df_merged_three["degree_diff"] / user_insulation_factor,
        axis=0
    )

    del df_merged_two, other_options, df_merged_three["degree_diff"]
    gc.collect()

    all_expenses = []
    for building_type in df_buildings_consumptions["building_type"].unique():
        df_dpe_building_type = df_buildings_consumptions[
            df_buildings_consumptions["building_type"] == building_type
        ]
        for dpe_class in df_dpe_building_type["dpe_class"].unique():
            df_temp = df_merged_three.copy(deep=True)
            dpe_value = df_dpe_building_type.loc[
                df_dpe_building_type["dpe_class"] == dpe_class, "consumption_in_kwh_per_square_meter"
            ].values[0]
            df_temp[all_options] = df_temp[all_options].multiply(dpe_value)
            df_temp["building_type"] = building_type
            df_temp["dpe_class"] = dpe_class
            all_expenses.append(df_temp)

    df_expenses = pd.concat(all_expenses, ignore_index=True)
    gc.collect()

    columns_reordered = [
        "date_time", "weather_description", "option_0", "option_1", "option_2", "option_3", "option_4", "building_type",
        "dpe_class"]

    return df_expenses[columns_reordered]
