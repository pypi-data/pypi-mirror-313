import pandas as pd


def set_edf_prices():
    """
    Set EDF electricity prices for different subscriptions.

    Returns:
        pd.DataFrame: DataFrame of subscription types with their respective kWh prices for normal and peak hours.
    """
    return pd.DataFrame({
        "subscription": ["Base", "Heures Creuses - Heures Pleines"],
        "kwh_price_normal_hour": [25.16, 20.68],
        "kwh_price_peak_hour": [25.16, 27.00]
    })
