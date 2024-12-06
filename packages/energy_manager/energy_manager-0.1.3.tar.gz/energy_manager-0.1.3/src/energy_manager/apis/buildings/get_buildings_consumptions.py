import requests
import pandas as pd
from typing import Optional

from energy_manager.utils.set_dpe_mappings import set_dpe_mappings
from energy_manager.apis.buildings.get_department import get_department


def get_buildings_consumptions(city_name: str) -> Optional[pd.DataFrame]:
    """
    Fetches buildings DPE data from the OpenDataSoft API for a given city,
    then converts it into an energy consumption per square meter.

    Args:
        city_name (str): Name of the city.

    Returns:
        Optional[pd.DataFrame]: DataFrame with buildings DPE data, or None if the fetch fails.
    """
    base_url = ("https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
                "base-des-diagnostics-de-performance-energetique-dpe-des-batiments-residentiels-p/records")
    department_name = get_department(city_name=city_name)
    if department_name:
        params = {
            "select": "classe_energie,"
                      " tr002_type_batiment_id",
            "where": f"annee_construction is not null and "
                     f"annee_construction >= date'2000' and "
                     f"classe_energie is not null and "
                     f"surface_habitable is not null and "
                     f"(tr002_type_batiment_id = \"Appartement\" or "
                     f"tr002_type_batiment_id = \"Maison\" or "
                     f"tr002_type_batiment_id = \"Logements collectifs\") and "
                     f"nom_dep = \"{department_name}\" and "
                     f"(classe_energie = \"A\" or "
                     f"classe_energie = \"B\" or "
                     f"classe_energie = \"C\" or "
                     f"classe_energie = \"D\" or "
                     f"classe_energie = \"E\" or "
                     f"classe_energie = \"F\")",
            "group_by": "classe_energie, tr002_type_batiment_id"
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            if data["results"]:
                new_data = pd.DataFrame(data["results"])

                new_data.rename(
                    columns={
                        "classe_energie": "dpe_class", "tr002_type_batiment_id": "building_type"
                    }, inplace=True)
                new_data["building_type"] = new_data["building_type"].astype(str)
                new_data["dpe_class"] = pd.Categorical(
                    new_data["dpe_class"], categories=["A", "B", "C", "D", "E", "F"], ordered=True)

                dpe_mappings = set_dpe_mappings()
                new_data["consumption_in_kwh_per_square_meter"] = new_data["dpe_class"].apply(
                    lambda x: dpe_mappings.get(x, None)).astype(float) / (365*24)

                return new_data
            print(f"No infos on buildings energy consumption found for the city {city_name}.")
            return None
        print(f"Error fetching data: {response.status_code}")
        return None
    print(f"No department found for city {city_name}.")
    return None
