import numpy as np
import pandas as pd
import xarray as xr



def calculate_max_installed_by_area(model_parameters):
    # Dictionnaire des technologies contrôlables
    controlable = {}
    controlable["electricity"] = [
        'ocgt', 'ccgt', 'ocgt_h2', 'ccgt_h2', 'biomass', 'coal',
        'lignite', 'hydro_reservoir', 'hydro_river', 'old_nuke', 'new_nuke'
    ]
    controlable["hydrogen"] = [
        'electrolysis', 'smr', 'smr_ccs', 'smr_partial_ccs',
        'atr', 'atr_ccs'
    ]

    # Création de filtered_max_install
    filtered_max_install = {
        'electricity': model_parameters["conversion_max_install_capacity"].sel(
            conversion_tech=[tech for tech in controlable["electricity"] if
                             tech in model_parameters["conversion_max_install_capacity"].conversion_tech.values]),
        'hydrogen': model_parameters["conversion_max_install_capacity"].sel(
            conversion_tech=[tech for tech in controlable["hydrogen"] if
                             tech in model_parameters["conversion_max_install_capacity"].conversion_tech.values])
    }

    # Calculer la somme par région pour chaque type de technologie contrôlable
    sum_max_install_by_area = {
        'electricity': filtered_max_install['electricity'].sum(dim=['conversion_tech', 'year_inv']),
        'hydrogen': filtered_max_install['hydrogen'].sum(dim=['conversion_tech', 'year_inv'])
    }

    # Convertir le résultat en DataFrame avec 'resource' comme colonne
    df_sum_max_install_by_area = pd.DataFrame({
        'area': model_parameters["conversion_max_install_capacity"].area.values,
        'electricity': sum_max_install_by_area['electricity'].values,
        'hydrogen': sum_max_install_by_area['hydrogen'].values
    })
    df_sum_max_install_by_area = df_sum_max_install_by_area.melt(id_vars=['area'], var_name='resource',
                                                                 value_name='max_install')

    demand_max = model_parameters["demand"].max(dim="hour", skipna=True).to_dataframe().dropna()

    #df_sum_max_install_by_area = calculate_sum_max_install_by_area(model_parameters)
    merged_df = demand_max.merge(df_sum_max_install_by_area, on=['area', 'resource'], how='left').set_index(
        ["area", "resource"])  / 1000
    merged_df.rename(columns={'demand': 'max_demand_GW', 'max_install': 'max_installed_controlable_prod_GW'}, inplace=True)

    return merged_df
