import pandas as pd
import xarray as xr

# from polars.testing.parametric import columns


def simplify_from_postfix(dataset, postfixes, name):
    """
    for postfix in postfixes this function looks at the dimension names
    of a dataset and if one ends with the value of postfix it simplfies its name to only postfix
    if no dimension has name postfix then it adds a dimension with only postfix and fill it with value of name
    typical use is with postfix = 'tech'
    Parameters
    ----------
    dataset
    postfixes
    name

    Returns
    -------

    """
    if isinstance(dataset, pd.DataFrame):
        dataset = dataset.squeeze().to_xarray()
    for postfix in postfixes:
        tech_dims = [dim for dim in dataset.dims if dim.endswith(postfix)]
        if len(tech_dims) == 0:
            dataset = dataset.expand_dims({postfix: [name]})
        elif len(tech_dims) == 1:
            dataset = dataset.rename({tech_dims[0]: postfix})
        else:
            raise ValueError(
                f"Dataset has more than one dimension ending with '{postfix}'. Unable to proceed."
            )

    return dataset


def reindex_by_area(dataset, transport_area_from, transport_area_to):
    """
    this function transforms a dataset initially indexed by "link" into a dataset indexed by "area"
    the dataset can either be a dataFrame or an xarray
    index association is described in transport_area_from and transport_area_to
    the result is indexed by area_from and area_to plus all other indexes

    Parameters
    ----------
    dataset
    transport_area_from
    transport_area_to

    Returns
    -------
    a data_frame
    Exemples
    >>>> exchange = solution.operation_transport_power_capacity.to_dataframe().groupby(['link','transport_tech', 'year_op']).sum()
    >>>> reindex_by_area(exchange, parameters['transport_area_from'], parameters['transport_area_to'])
    """

    input_type_of_dataset = xr.DataArray
    if isinstance(dataset, pd.DataFrame):
        dataset = dataset.squeeze().to_xarray()
        input_type_of_dataset = pd.DataFrame
    input_name = dataset.name
    indexes = list(dataset.coords)
    indexes_without_link = [x for x in indexes if x != "link"]
    if "transport_tech" in transport_area_from.coords:
        reindexed_dataset = dataset.assign_coords(
            area_from=(["link", "transport_tech"], transport_area_from.data),
            area_to=(["link", "transport_tech"], transport_area_to.data),
        )
    else:
        reindexed_dataset = dataset.assign_coords(
            area_from=(["link"], transport_area_from.data),
            area_to=(["link"], transport_area_to.data),
        )

    reindexed_dataset_s = (
        reindexed_dataset.to_dataframe()
        .reset_index()
        .set_index(["area_from", "area_to"] + indexes_without_link)[[input_name]]
    )

    return reindexed_dataset_s


def aggregate_link_data(dataset, stacked_into_transport_tech=False, output_name=None):
    """
    Input dataset (dataframe or xarray) is indexed by area_from and area_to (and other indexes).
    Tipically the output of function reindex_by_area.
    calculates the sum of incoming and outcoming power (capacity or energy flow per hour).
    the output is indexed by area only but has two columns, one with _outgoing postfix and one with _incoming postfix.
    an option is available to stack the results in one column and indicate incomming / outgoing as a postfix to transport_tech
    Returns
    a dataframe of a xarray
    -------
    Exemples
    >>>> exchange = solution.operation_transport_power_capacity.to_dataframe().groupby(['link','transport_tech', 'year_op']).sum()
    >>>> exchange_ri = reindex_by_area(exchange, parameters['transport_area_from'], parameters['transport_area_to'])
    >>>> aggregate_link_data(exchange_ri)
    >>>> aggregate_link_data(exchange_ri,stacked_into_transport_tech=True)
    """

    input_name = dataset.columns[0]
    if output_name is None:
        output_name = input_name
    incoming_power = dataset.groupby(
        [col for col in dataset.reset_index().columns if (col != "area_to" and col != input_name)]
    ).sum()
    incoming_power = incoming_power.rename(
        columns={input_name: output_name + "_total_incoming"}
    ).rename_axis(index={"area_from": "area"})
    outgoing_power = dataset.groupby(
        [col for col in dataset.reset_index().columns if (col != "area_from" and col != input_name)]
    ).sum()
    outgoing_power = outgoing_power.rename(
        columns={input_name: output_name + "_total_outgoing"}
    ).rename_axis(index={"area_to": "area"})
    aggregated_reindexed_dataset = pd.merge(
        outgoing_power, incoming_power, left_index=True, right_index=True
    )

    if stacked_into_transport_tech:
        aggregated_reindexed_dataset = aggregated_reindexed_dataset.stack().reset_index()
        indexes = list(aggregated_reindexed_dataset.columns[:-2])
        aggregated_reindexed_dataset.columns = indexes + ["direction", output_name]
        aggregated_reindexed_dataset["transport_tech"] = (
            aggregated_reindexed_dataset["transport_tech"]
            + "_"
            + aggregated_reindexed_dataset["direction"].map(get_last_word)
        )
        aggregated_reindexed_dataset = aggregated_reindexed_dataset.drop(
            columns=["direction"]
        ).set_index(indexes)

    return aggregated_reindexed_dataset


def get_previous_word(input_str, type):
    """

    Parameters
    ----------
    input_str
    type

    Returns
    -------

    """
    # removes "type" from the end of the string if it exists
    if input_str.endswith("_" + type):
        input_str = input_str[: -(len(type) + 1)]

    # words = input_str.split('_')
    # return words[-1] if words else None
    return input_str


def calculate_total_power_capacity(solution, parameters, by_year_op=True, by_area=True):
    """
    compute all power capacities, eventually aggregated by year_op or area.
    ## should replace get_capacities, see calculate_total_of_a_type

    Parameters
    ----------
    solution
    parameters
    by_year_op
    by_area

    Returns
    -------

    Examples:
        >>>     model = build_model(parameters)
        >>> model.solve(solver_name="highs")
        >>> p = model.parameters
        >>> s = model.solution
        >>> calculate_total_power_capacity(s, p)
        >>> calculate_total_power_capacity(s, p, by_area=False)
        >>> calculate_total_power_capacity(s, p, by_year_op=False)
    """
    return calculate_total_of_a_type(
        "power_capacity", solution, parameters, by_year_op=by_year_op, by_area=by_area
    )


def calculate_total_costs(solution, parameters, by_year_op=True, by_area=True):
    """
    compute all costs, eventually aggregated by year_op or area.
    ## should replace get_costs, see calculate_total_of_a_type
    Parameters
    ----------
    solution
    parameters
    by_year_op
    by_area

    Returns
    -------

    """
    total_costs = {}
    total_costs["operation"] = calculate_total_of_a_type(
        "costs",
        solution,
        parameters,
        operation_or_planning="operation",
        by_year_op=by_year_op,
        by_area=by_area,
    )
    total_costs["planning"] = calculate_total_of_a_type(
        "costs",
        solution,
        parameters,
        operation_or_planning="planning",
        by_year_op=by_year_op,
        by_area=by_area,
    )

    total_costs["planning"] =  total_costs["planning"].reorder_levels(
        order=total_costs["operation"].index.names
    )

    return pd.concat(total_costs.values(), keys=total_costs.keys(), names=["operation_or_planning"])


def calculate_total_net_generation(solution, parameters, by_year_op=True, by_area=True):
    """
    compute all net_generation, eventually aggregated by year_op or area.
    ## should replace get_net_generation, see calculate_total_of_a_type

    Parameters
    ----------
    solution
    parameters
    by_year_op
    by_area

    Returns
    -------

    """
    return calculate_total_of_a_type(
        "net_generation", solution, parameters, by_year_op=by_year_op, by_area=by_area
    )


def calculate_total_emissions(solution, parameters, by_year_op=True, by_area=True):
    """
    compute all emissions, eventually aggregated by year_op or area.

    Parameters
    ----------
    solution
    parameters
    by_year_op
    by_area

    Returns
    -------

    """
    return calculate_total_of_a_type(
        "emissions", solution, parameters, by_year_op=by_year_op, by_area=by_area
    )


def get_last_word(input_str, sep="_"):
    """

    Parameters
    ----------
    input_str
    sep

    Returns
    -------

    """
    words = input_str.split(sep=sep)
    return words[-1] if words else None


def get_sum_dims(variable, by_year_op=True, by_area=True):
    """
    compute a list of coordinates to sum on (all others will be kept)
    Parameters
    ----------
    solution
    by_year_op
    by_area

    Returns
    -------

    """
    sum_dims = []
    if "year_inv" in variable.dims:
        sum_dims.append("year_inv")
    if "hour" in variable.dims:
        sum_dims.append("hour")
    if not by_year_op and "year_op" in variable.dims:
        sum_dims.append("year_op")
    if not by_area and "area" in variable.dims:
        sum_dims.append("area")
    return sum_dims


def calculate_total_of_a_type(
    type, solution, parameters, operation_or_planning="operation", by_year_op=True, by_area=True
):
    """
    This function calculates total power capacity or total net_generation or total costs depending on the value of type and over variables prefixed with operation_or_planning.
    re-indexation of link index is performed, and variables names are simplified to fit in a simple panda table
    by default the sum is computed by year_op and by area but two parameters allow to modify that.
    type can be 'power_capacity'
    operation_or_planning should be "operation" or "planning"
    not possible : type=="net_generation" and operation_or_planning=="planning"

    It replaces
    - get_capacities(solution, model_parameters) (with calculate_total_of_a_type("power_capacity", solution, model_parameters)
    - get_net_generation(solution, model_parameters) (with calculate_total_of_a_type("net_generation", solution, model_parameters)
    - get_costs(solution, model_parameters) (with calculate_total_of_a_type("costs", solution, model_parameters,operation_or_planning="operation")
    of operation_or_planning="planning" for planning costs
    Parameters
    ----------
    type
    solution
    parameters
    operation_or_planning
    by_year_op
    by_area

    Returns
    -------

    """

    try:
        variables_of_type_type = [
            var
            for var in solution.data_vars
            if var.startswith(operation_or_planning + "_") and var.endswith("_" + type)
        ]
        calculated_total_dict = {}
        for var in variables_of_type_type:
            variable_name = get_previous_word(var.replace(operation_or_planning + "_", ""), type)
            sum_dims = get_sum_dims(solution[var], by_year_op, by_area)

            calculated_total = solution[var].sum(dim=sum_dims)
            if type == "costs" and variable_name == "net_import":
                calculated_total = calculated_total.rename({"resource": "tech"})

            ## rearrangement
            if "link" in solution[var].dims:
                calculated_total = reindex_by_area(
                    calculated_total,
                    parameters["transport_area_from"],
                    parameters["transport_area_to"],
                )
                calculated_total = aggregate_link_data(
                    calculated_total, stacked_into_transport_tech=True, output_name=type
                )

            else:
                calculated_total = calculated_total

            calculated_total = simplify_from_postfix(
                calculated_total, postfixes=["tech"], name=variable_name
            )
            calculated_total = calculated_total.to_dataframe(name=type)
            if var == variables_of_type_type[0]:
                calculated_total_dict[variable_name] = calculated_total
                initial_calculated_total = calculated_total
            else:
                if isinstance(calculated_total.index, pd.MultiIndex):
                    calculated_total = calculated_total.reorder_levels(
                        order=initial_calculated_total.index.names
                    )
                    calculated_total = calculated_total.sort_index()
                    calculated_total_dict[variable_name] = calculated_total.reorder_levels(
                        order=initial_calculated_total.index.names
                    )
                else:
                    calculated_total_dict[variable_name] = calculated_total
        # Convert dictionary of DataFrames to a single DataFrame while keeping original indexes
        combined_df = pd.concat(
            calculated_total_dict.values(),
            keys=calculated_total_dict.keys(),
            names=["type"],
            sort=False,
            join="outer",
            ignore_index=False,
        )
        combined_df.index.set_names(
            ["type"] + list(calculated_total_dict.values())[0].index.names, inplace=True
        )
        combined_df = combined_df.sort_index()  # Ensure consistent ordering of multi-index levels

        return combined_df

    except KeyError as e:
        print(e)


def generate_summary_dataframes_from_results(solution, parameters, by_year_op=True, by_area=True):
    """
    Generate dataframes based on the data from the study results.

    Parameters:
    study_results (Path): Path to the directory containing the study results CSV files.

    Returns:
    dict: A pandas DataFrames, each representing a different aspect of the study results.

    Examples
    >>>>>>
    >>>>>>  generate_summary_dataframes_from_results(solution,parameters)
    """

    dataframes = {}
    dataframes["Operation costs - EUR"] = solution.annualised_totex
    dataframes["Production capacity - MW"] = calculate_total_power_capacity(
        solution, parameters, by_year_op=by_year_op, by_area=by_area
    )
    dataframes["Total costs - EUR"] = calculate_total_costs(
        solution, parameters, by_year_op=by_year_op, by_area=by_area
    )
    dataframes["CO2 emissions - tCO2eq"] = calculate_total_emissions(
        solution, parameters, by_year_op=by_year_op, by_area=by_area
    )
    dataframes["Production - MWh"] = calculate_total_net_generation(
        solution, parameters, by_year_op=by_year_op, by_area=by_area
    )

    variables_dict = {
        "demand": "Demand - MWh",
        "operation_storage_energy_capacity": "Storage capacity - MWh",
        "operation_spillage": "Spillage - MWh",
        "operation_curtailment": "Loss of load - MWh",
    }
    for key in variables_dict:
        if key in solution.dims:
            sum_dims = get_sum_dims(solution[key], by_year_op=by_year_op, by_area=by_area)
            dataframes[variables_dict[key]] = solution.key.sum(sum_dims).to_dataframe()
        if key in parameters.dims:
            sum_dims = get_sum_dims(parameters[key], by_year_op=by_year_op, by_area=by_area)
            dataframes[variables_dict[key]] = parameters.key.sum(sum_dims).to_dataframe()

    return dataframes


def write_to_excel(dataframes, excel_file):
    """
    Write the dataframes to an Excel file.

    Parameters:
    dataframes (dict): A dictionary of pandas DataFrames to be written to the Excel file.
    excel_file (Path): Path to the Excel file where dataframes will be written.
    """
    with pd.ExcelWriter(excel_file.name) as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
