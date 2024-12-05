import datetime
import logging
import os

import numpy as np
import pandas as pd
import xarray as xr


def sort_dataset(ds):
    ds_ = ds[sorted(ds.dims) + sorted(ds.data_vars)]
    ds_ = ds_.transpose(*ds_.dims)
    return ds_


def array_to_datetime(hours, year=2000, datetime_format="%d/%m %H:%M"):
    h0 = datetime.datetime(year=year, month=1, day=1)
    return np.vectorize(
        lambda hour: (h0 + datetime.timedelta(hours=int(hour))).strftime(datetime_format),
    )(hours)


def model_solve(model_, solver):
    if solver == "gurobi":
        model_.solve(solver_name=solver, method=2, crossover=0)  # crossover=0, numericfocus=3)
    elif solver == "highs":
        model_.solve(
            solver_name=solver,
            presolve="on",
            solver="ipm",
            parallel="on",
            run_crossover="on",
            ipm_optimality_tolerance=1e-8,
        )
    elif solver == "xpress":
        model_.solve(solver_name=solver, DEFAULTALG=4, CROSSOVER=2)
    else:
        model_.solve(solver_name=solver)
    return model_


def crf(r, m):
    """
    Compute the capital recovery factor.

    Parameters
    ----------
    r : float
        The finance rate between two terms.

    m : int
        The number of terms.

    Returns
    -------
    float
        The capital recovery factor or a NaN value if the number of terms is not strictly positive.
    """
    if m <= 0:
        return np.nan
    if r == 0:
        return 1 / m
    return r / (1 - (1 + r) ** (-np.array(m, dtype=np.float64)))


def discount_factor(r, year, year_ref):
    """
    Compute the discount factor from year to _year_ref.

    Parameters
    ----------
    r : float
        Discount rate.

    year : int
        Year when the cash flow occurs.

    year_ref : int
        The year to discount the cash flows to.

    Returns
    -------
    float
        The discount factor from year to year_ref.
    """
    return (1 + r) ** (-np.array(year - year_ref, dtype=np.float64))


def square_array_by_diagonals(shape, diags, fill=0, dtype=None):
    """
    Build a square numpy float array diagonal by diagonal with the numpy diag function and
    fill other values with fill parameter.

    Based on numpy diag method.

    Parameters
    ----------
    shape : int
        The shape of the square array.

    diags : dict
        Dictionnary with the index of the diagonal as key and the value floats/arrays as values.
        The default diagonal is indexed 0. Use `key>0` for diagonals above the main diagonal,
        and `key<0` for diagonals below the main diagonal. If value is scalar, the whole (sub-)diagonal
        will be filled with this value. If value is an 1-d array, the diagonal will be set to this value
        following numpy convention if sizes do not match.

    fill : float
        The fill value in the array. Can be NaN value.

    dtype : data-type, optional
        The desired data-type for the array, e.g., `numpy.int8`.  Default is
        `numpy.float64`.

    Returns
    -------
    out : ndarray
        The constructed diagonal by diagonal square array.

    Examples
    --------
        >>> dict_diag = {0: 5, 1: [1, 2], -2:[1, 2, 3]}
        >>> square_array_by_diagonals(shape=5, diags=dict_diag, fill=np.nan)
        array([[ 5.,  1., nan, nan, nan],
               [nan,  5.,  2., nan, nan],
               [ 1., nan,  5.,  1., nan],
               [nan,  2., nan,  5.,  2.],
               [nan, nan,  3., nan,  5.]])

    """
    res = np.zeros((shape, shape), dtype=dtype)
    res.fill(fill)
    for k, value in diags.items():
        if k >= 0:
            i = k
        else:
            i = (-k) * shape
        res[: shape - k].flat[i :: shape + 1] = value
    return res


def combine_csv_to_excel(repo_path, output_excel_path, sep=";"):
    """
    Combine multiple CSV files from a repository into a single Excel file.

    Parameters
    ----------
    repo_path : str
        The path to the repository directory containing the CSV files.
    output_excel_path : str
        The path where the combined Excel file will be saved.
    sep : str, default ';'
        String of length 1. Field delimiter for the output file.

    Returns
    -------
    None
        The function does not return anything, it saves the combined Excel file to the specified path.

    Examples
    --------
    >>> repo = "/path/to/your/repository"
    >>> excel_path = "/path/to/output/output.xlsx"
    >>> combine_csv_to_excel(repo, excel_path)

    """
    csv_files = [file for file in os.listdir(repo_path) if file.endswith(".csv")]

    with pd.ExcelWriter(output_excel_path) as writer:
        for csv_file in csv_files:
            df = pd.read_csv(os.path.join(repo_path, csv_file), sep=sep)
            df.to_excel(writer, sheet_name=os.path.splitext(csv_file)[0], index=False)
    return None


def split_excel_to_csv(input_excel_path, output_folder, sep=";"):
    """
    Split an Excel file with multiple sheets into separate CSV files.

    Parameters
    ----------
    input_excel_path : str
        The path to the input Excel file.
    output_folder : str
        The path to the folder where the CSV files will be saved.
    sep : str, default ';'
        String of length 1. Field delimiter for the output file.

    Returns
    -------
    None
        The function does not return anything, it saves the separate CSV files to the specified folder.

    Examples
    --------
    >>> excel_path = "/path/to/input/input.xlsx"
    >>> folder = "/path/to/output/csv_files/"
    >>> split_excel_to_csv(excel_path, folder)

    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    excel_file = pd.ExcelFile(input_excel_path)

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        output_csv_path = os.path.join(output_folder, f"{sheet_name}.csv")
        df.to_csv(output_csv_path, index=False, sep=sep)
    return None


def get_main_resource(model_parameters):
    p = model_parameters

    storage = xr.DataArray([], coords=dict(tech=[]))
    transport = xr.DataArray([], coords=dict(tech=[]))

    conversion = p.resource.isel(resource=(p.conversion_factor == 1).argmax(dim="resource"))
    conversion = conversion.drop_vars("resource").rename(conversion_tech="tech")

    if "storage" in p.keys() and p.storage:
        storage = p.storage_main_resource.rename(storage_tech="tech")
    if "transport" in p.keys() and p.transport:
        is_link = p.transport_is_link.any(
            [dim for dim in p.transport_is_link.dims if "area" not in dim]
        )
        filter = is_link.sel(
            area_from=p.area_from.isel(area_from=0),
            area_to=p.area_to.sel(
                area_to=is_link.isel(area_from=0).where(is_link).sum("area_from") > 0
            ).isel(area_to=0),
        )
        transport = (
            p.isel(year_inv=0, drop=True)
            .transport_resource.sel(area_from=filter.area_from, area_to=filter.area_to, drop=True)
            .rename(transport_tech="tech")
        )

    da = xr.concat([conversion, storage, transport], dim="tech")

    return da


def squeeze_dataset(ds, exclude_dims=None, exclude_data_vars=None, copy=True):
    """
    Squeeze dimensions in the Dataset where all values are equal, with optional exclusions.

    This function inspects each variable in the Dataset and checks if all values
    along a dimension are identical. If so, that dimension is "squeezed" (i.e.,
    reduced to a single value). Optionally, specific dimensions or data variables
    can be excluded from this operation.

    Parameters
    ----------
    ds : xarray.Dataset
        The input Dataset containing data variables to be checked for squeezing.

    exclude_dims : list or None, optional
        A list of dimension names to exclude from squeezing. If None, no dimensions are excluded.

    exclude_data_vars : list or None, optional
        A list of data variable names to exclude from the squeezing operation.
        If None, all variables will be checked.

    copy : bool, optional
        If True (default), a copy of the dataset is made before squeezing. If False,
        the original dataset is modified in place.

    Returns
    -------
    xarray.Dataset
        A new Dataset where dimensions with identical values across their coordinates
        are squeezed, unless explicitly excluded.

    Notes
    -----
    - The function logs a warning for each squeezed dimension.
    - If `exclude_dims` or `exclude_data_vars` are not provided, the function will attempt
      to squeeze all dimensions and data variables.
    """
    if copy:
        ds = ds.copy(deep=True)
    for var_name in ds.data_vars:
        data_var = ds[var_name]
        if exclude_data_vars is None or data_var not in exclude_data_vars:
            for dim in data_var.dims:
                if exclude_dims is None or dim not in exclude_dims:
                    # Check if all values along the specified dimension are equal
                    if np.equal(data_var, data_var.isel({dim: 0})).all():
                        logging.warning(msg=f"squeezing dim {dim} in data_var {data_var.name}")
                        ds[var_name] = data_var.isel({dim: 0})
    return ds


def get_infeasibility_constraint_name(constraint_label, model, model_parameters):
    if isinstance(constraint_label, str):
        constraint_label = int(constraint_label[1:])
    p = model_parameters
    m = model
    constraint_name = m.constraints.get_name_by_label(constraint_label)
    constraint = m.constraints[constraint_name]
    index = {}
    for dim in list(constraint.coord_dims):
        index[dim] = p[dim].where(
            (constraint.labels == constraint_label).any(
                dim=[d for d in list(constraint.coord_dims) if d != dim]
            ),
            drop=True,
        )
        index[dim] = index[dim].to_numpy().astype(p[dim].dtype)[0]
    print(f"\n{constraint_name}\n" + "\n".join([f"{key}: {value}" for key, value in index.items()]))
    return constraint.sel(index)
