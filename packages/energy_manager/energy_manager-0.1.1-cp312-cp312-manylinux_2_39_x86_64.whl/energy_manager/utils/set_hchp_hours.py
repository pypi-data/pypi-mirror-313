import pandas as pd
from pathlib import Path

def set_hchp_hours():
    """
    Identify for a whole day which hours can be considered as 'Heures Creuses' or 'Heures Pleines' in France,
    based on ENEDIS proposals in the context of an EDF subscription for electricity.
    Returns:
        pd.DataFrame: A DataFrame containing the qualification of each hour (in 24-hour format) as 'Heures Creuses' or 'Heures Pleines'.
    """
    df_hchp_hours = pd.read_csv(filepath_or_buffer=Path(__file__).parent / "data/hchp_hours.csv")

    df_hchp_hours["hour"] =  df_hchp_hours["hour"].astype(int)
    df_hchp_hours[["option_1", "option_2", "option_3", "option_4"]] = (
        df_hchp_hours[["option_1", "option_2", "option_3", "option_4"]].astype(str))

    return df_hchp_hours
