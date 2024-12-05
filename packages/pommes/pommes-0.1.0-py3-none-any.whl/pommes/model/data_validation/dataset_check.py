import logging

import numpy as np

from pommes.model.data_validation import ref_inputs


def check_inputs(ds):
    """
    Validates and updates the input dataset by checking consistency with a reference configuration.

    Parameters
    ----------
    ds : xarray.Dataset
        Input dataset to be validated. Each variable in the dataset is checked
        against the reference configuration defined in "pommes/dataset_description.yaml".

    Raises
    ------
    ValueError
        If there are mismatches between the dataset's coordinates and types
        against the reference configuration.

    Warnings
    --------
    If any expected data variables are missing for a module, the dataset is updated
    with default values from the reference configuration.

    Notes
    -----
    - The function verifies that the coordinates and data types of the dataset's
      variables match the expected values from the reference file.
    - If any required data variables are missing from the dataset for a particular module,
      the function adds them with default values from the reference configuration.

    Returns
    -------
    xarray.Dataset
        The validated and updated dataset. If necessary, missing data variables are
        added with default values.
    """

    # Check type and coordinate consistency
    for variable in ds.data_vars:
        da = ds[variable]

        if not set(da.coords).issubset(ref_inputs[variable]["index_set"]):
            raise ValueError(
                f"For data variable {variable}: \n{list(da.coords)} not in {ref_inputs[variable]['index_set']}"
            )

        if not isinstance(da.dtype, type(np.dtype(ref_inputs[variable]["type"]))):
            try:
                ds[variable] = ds[variable].astype(ref_inputs[variable]["type"])
                logging.warning(
                    f"Data variable {variable}: \nGiven type is {da.dtype} and is converted to {ref_inputs[variable]['type']}"
                )
            except ValueError as e:
                print(e.args[0])
                raise ValueError(
                    f"For data variable {variable}: \nGiven type is {da.dtype} and should be {ref_inputs[variable]['type']}"
                )
    # Check the presence of all data variables for all present modules
    modules = ["carbon", "combined", "conversion", "transport", "net_import", "storage", "turpe"]
    variables = list(ref_inputs.keys())
    for module in modules:
        if module not in ds.data_vars or not ds[module]:
            variables = [var for var in variables if module not in var]

    for variable in ds.data_vars:
        if variable in variables:
            variables.remove(variable)

    if len(variables) > 0:
        logging.warning(
            f"Data variables not in input dataset \nUpdating dataset with default values\n"
            + (
                "\n".join(
                    [
                        f"{variable}: {ref_inputs[variable]['default']}, type = {ref_inputs[variable]['type']}"
                        for variable in variables
                    ]
                )
            )
        )
        for variable in variables:
            ds = ds.assign(
                {
                    variable: np.array(
                        ref_inputs[variable]["default"], dtype=ref_inputs[variable]["type"]
                    )
                }
            )

    # Year_dec is big enough for decommissioning

    life_span_vars = [data_var for data_var in ds.data_vars if "life_span" in data_var]
    max_life_span = np.array(
        ds[life_span_vars].to_dataarray(name="tech").to_dataframe().max().iloc[0]
    )

    if max_life_span + ds.year_inv.max() > ds.year_dec.max():
        raise ValueError(
            f"max life span is {max_life_span} \n"
            f"Max year_inv is {int(ds.year_inv.max())} \n"
            f"Max year_dec is {int(ds.year_dec.max())}"
        )

    # Check consistency of coupled data_variables
    # TODO: Check annuity computation
    #     for variable in ds.data_vars:
    #         if "annuity" in variable and not np.any(np.logical_not(np.isnan(ds[variable]))):
    #             pass
    # TODO: Check discount computation

    return ds
