import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
import yaml

from pommes.utils import crf, discount_factor


def read_config_file(filename="config", file_path=None, study=None):
    """
    Reads the configuration file for a study.

    Parameters
    ----------
    filename : str, optional
        Name of the config file without the ".yaml" extension. If not provided, default value is "config".
    file_path : str, optional
        Path to the configuration file. If not provided, default value is None.
    study : str, optional
        Name of the study. If not provided, default value is None.Must be given if file_path is None

    Returns
    -------
    dict
        Dictionary containing the configuration of the study.
    """
    if file_path is None:
        file_path = f"study/{study}/{filename}.yaml"
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    if data["input"].get("path") is None:
        data["input"]["path"] = Path(file_path).parent / "data"

    else:
        if (data["input"]["path"] != f"study/{study}/data") and (study is not None):
            warnings.warn(
                f"Config seems to be inconsistent with study name: \n "
                f"Study name '{study}' \n "
                f"Config path: '{data['input']['path']}'",
            )

    return data


def build_coordinates(config_):
    """
    Build coordinates based on the configuration.

    Parameters
    ----------
    config_ : dict
        Configuration dictionary.

    Returns
    -------
    xarray.Coordinates
        Xarray coordinates constructed from the configuration.
    """
    return xr.Coordinates(
        {
            coord_label: np.array(x["values"], dtype=x["type"])
            for coord_label, x in config_["coords"].items()
        }
    )


def load_inputs_as_dict_of_df(config_):
    """
    Loads input data from all CSV files given in data variable descriptions.

    Parameters
    ----------
    config_ : dict
        Configuration dictionary.

    Returns
    -------
    dict of pandas.DataFrame
        Dictionary of DataFrame containing the loaded data.
    """
    parameters = config_["input"]["parameters"]
    path = config_["input"]["path"]

    file_index = {}

    for variable in parameters.keys():
        file = parameters[variable]["file"]
        index_input = parameters[variable]["index_input"]
        if file in file_index.keys():
            if file_index[file] != tuple(sorted(index_input)):
                raise ValueError(
                    f"Same file has not identical index in data variable descriptions!\n"
                    f'Check index of variable "{variable}".'
                )
        else:
            file_index[file] = tuple(sorted(index_input))

    dict_df = {
        file: pd.read_csv(
            f"{path}/{file}",
            index_col=index_input,
            dtype={coord: np.dtype(config_["coords"][coord]["type"]) for coord in index_input},
            sep=";",
        )
        for (file, index_input) in file_index.items()
    }
    return dict_df


def compute_end_of_life(ds):
    for data_var in ds.data_vars:
        if "life_span" in data_var:
            ds[data_var.replace("life_span", "end_of_life")] = (
                ds.year_dec.broadcast_like(ds.year_inv + ds[data_var])
                .where(ds.year_dec <= (ds.year_inv + ds[data_var]))
                .max("year_dec")
                .astype("int64")
            )
    return ds


def build_annuity_rate(
    years_dec_,
    years_inv_,
    max_finance_rate=0.1,
    finance_rate_step=0.005,
):
    """
    Build a DataArray containing capital recovery factor (or annuity rate) for financial data

    Parameters
    ----------
    years_dec_ : xr.DataArray
        Decommissioning year coordinates.

    years_inv_ : xr.DataArray
        Investment year coordinates.

    max_finance_rate : float, optional
        Maximum financing rate. Default is 0.1.

    finance_rate_step : float, optional
        Step size for financing rate. Default is 0.005.

    Returns
    -------
    xr.DataArray
        DataArray containing the repayment rates indexed with financing rates in [[0, max_finance_rate]]
        with step finance_rate_step,  decommissioning year and investment year.
    """
    temp = np.arange(0, max_finance_rate, finance_rate_step, dtype="float64")
    finance_rate = xr.DataArray(temp, coords=dict(finance_rate=temp))

    df = (
        xr.DataArray(np.nan, coords=[years_dec_, years_inv_, finance_rate])
        .to_dataframe(name="crf")
        .reset_index()
    )

    df["crf"] = df.apply(lambda row: crf(row.finance_rate, row.year_dec - row.year_inv), axis=1)
    return df.set_index(["year_dec", "year_inv", "finance_rate"]).to_xarray().crf


def compute_annuity_cost(ds, config_):
    annuity_rate = build_annuity_rate(ds.year_inv, ds.year_dec)
    annuity_to_compute = config_["pre_process"]["annuity_computation"]

    for category, dict_annuity in annuity_to_compute.items():
        if ds[category].any():
            for name, param in dict_annuity.items():
                ds = ds.assign(
                    {
                        name: ds[param["invest_cost"]]
                        * xr.where(
                            cond=(
                                (ds.year_inv < ds.year_dec)
                                * (ds.year_dec <= (ds.year_inv + ds[param["life_span"]]))
                                * np.isfinite(ds[param["finance_rate"]])
                            ),
                            x=annuity_rate.sel(
                                finance_rate=ds[param["finance_rate"]].where(
                                    ds[param["finance_rate"]].isin(annuity_rate.finance_rate),
                                    0,
                                )
                            ).drop_vars("finance_rate"),
                            y=np.nan,
                        )
                    }
                )
    return ds


def compute_discount(ds, config_):
    """

    Returns
    -------
    xr.DataArray
        DataArray containing the discount rate from each operation years to the reference year.
    """

    discount_rate = ds[config_["pre_process"]["discount_factor"]["discount_rate"]]
    year_ref = ds[config_["pre_process"]["discount_factor"]["year_ref"]]

    discount_rate = xr.broadcast(xr.DataArray(discount_rate), ds.year_op)[0]

    ds = ds.assign(
        discount_factor=xr.DataArray(
            np.array(
                np.vectorize(discount_factor, excluded=["year_ref"])(
                    r=discount_rate, year=ds.year_op.astype(np.float64), year_ref=year_ref
                ),
                dtype=np.float64,
            ),
            coords=[ds.year_op],
        )
    )

    return ds


def build_input_parameters(config_):
    """
    Constructs and validates the input parameters for a simulation based on the given configuration.

    Parameters
    ----------
    config_ : dict
        Configuration dictionary containing information about input parameters, modules,
        and coordinate types. This dictionary typically includes:
        - `input["parameters"]`: A dictionary where each parameter is defined by
          its file source, column, data type, index set, and fill values.
        - `add_modules`: A dictionary indicating which modules to include in the dataset.
        - `coords`: The coordinate information and data types.

    Raises
    ------
    ValueError
        If there is an inconsistency between the index input and index set for any parameter.

    Returns
    -------
    xarray.Dataset
        The dataset built from the input parameters, with modules, coordinates, and
        parameters set according to the configuration. Missing data is filled with
        default values where necessary, and annuity cost and discount values are computed.

    Notes
    -----
    - This function first builds the dataset coordinates and assigns modules based on the
      `config_` dictionary.
    - Parameters are validated against their expected index sets. If there is any inconsistency,
      a `ValueError` is raised.
    - The parameter data is loaded from the source files and columns, cast to the required data
      type, and broadcast to match the dataset's coordinates.
    - Any missing data in the parameter arrays is filled with the specified fill values.
    - After assigning all parameters, additional computations for annuity costs and discounting
      are performed using `compute_annuity_cost` and `compute_discount`.
    """

    parameters = config_["input"]["parameters"]

    dict_df = load_inputs_as_dict_of_df(config_)
    ds = xr.Dataset(coords=build_coordinates(config_))

    for module, boolean in config_["add_modules"].items():
        ds = ds.assign({module: boolean})

    for key, param in parameters.items():
        series = dict_df[param["file"]][param["column"]].astype(param["type"])

        if series.index.names[0] is None:
            da = xr.DataArray(np.array(series[0]))
        else:
            da = series.to_xarray().astype(param["type"])
            da = da.broadcast_like(ds[list(da.dims)])
            da = da.assign_coords(
                {coord: da[coord].astype(config_["coords"][coord]["type"]) for coord in da.dims}
            )

        if np.any(da.isnull()):
            da = da.fillna(np.array(param["fill"], dtype=param["type"]))
        ds = ds.assign({key: da})

    ds = compute_end_of_life(ds)
    ds = compute_annuity_cost(ds, config_)
    ds = compute_discount(ds, config_)

    return ds
