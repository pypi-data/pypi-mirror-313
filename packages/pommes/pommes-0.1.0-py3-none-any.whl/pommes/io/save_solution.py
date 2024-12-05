import os

import pandas as pd
import yaml


def save_solution(model, output_folder, export_csv=True, save_input=True, model_parameters=None):
    """
    Save the solution of a Linopy optimization model.

    Parameters
    ----------
    model : Linopy.Model
        The Linopy optimization model containing the solution to be saved.

    output_folder : str
        The name of the output directory

    model_parameters : ModelParameters, optional
        The object containing all the data needed to build the model. Must be given if save_input=True
        Default is None

    export_csv : bool, optional
        Flag indicating whether to export the solution to CSV files. Defaults to True.

    save_input : bool, optional
        Flag indicating whether to duplicate the input in CSV files. Defaults to True.

    Returns
    -------
    None

    Notes
    -----
    This function saves the solution of a Linopy optimization model to binary and CSV files.
    The solution includes variable values, dual values of constraints, and the objective value.

    The saved files are organized in the following directory structure:
    - `output/{scenario}_{suffix}/variables/`: Directory containing CSV files with variable values.
    - `output/{scenario}_{suffix}/constraints/`: Directory containing CSV files with dual values of
    constraints.
    - `output/{scenario}_{suffix}/solution_dual_objective_value.pkl`: Binary file containing a pickled
    object with the model solution.
    """

    if not os.path.exists(f"{output_folder}/"):
        os.makedirs(f"{output_folder}/")

    model.to_netcdf(f"{output_folder}/model.nc", format="NETCDF4")

    if save_input:
        if model_parameters is None:
            raise ValueError(f"Cannot save inputs as model_parameters is None.")
        else:
            model_parameters.to_netcdf(f"{output_folder}/input.nc", format="NETCDF4")

            if not os.path.exists(f"{output_folder}/inputs/"):
                os.makedirs(f"{output_folder}/inputs/")
            not_df = {}
            for label, param in model_parameters.items():
                try:
                    param.to_dataframe().dropna(axis=0).rename(columns={"value": label}).to_csv(
                        f"{output_folder}/inputs/{label}.csv", sep=";"
                    )
                except ValueError:
                    not_df[label] = param.to_numpy()[()]

            with open(f"{output_folder}/inputs/other_param.yaml", "w") as outfile:
                yaml.dump(not_df, outfile)

            # TODO: format="NETCDF4"

    model.constraints.dual.to_netcdf(f"{output_folder}/dual.nc")
    model.solution.to_netcdf(f"{output_folder}/solution.nc")
    obj = pd.Series(dict(objective=model.objective.value))
    obj.to_csv(f"{output_folder}/objective.csv", sep=";")

    if export_csv:
        dual = {}
        for label, constraint in model.constraints.items():
            dual[label] = constraint.dual.to_dataset(name=label)

        # Create output directories
        if not os.path.exists(f"{output_folder}/variables/"):
            os.makedirs(f"{output_folder}/variables/")
        if not os.path.exists(f"{output_folder}/constraints/"):
            os.makedirs(f"{output_folder}/constraints/")

        # Write CSV files
        for label, variable in model.variables.items():
            variable.solution.to_dataframe().dropna(axis=0).rename(
                columns={"solution": label}
            ).to_csv(f"{output_folder}/variables/{label}.csv", sep=";")
        for label, constraint in dual.items():
            dual[label].to_dataframe().dropna(axis=0).to_csv(
                f"{output_folder}/constraints/{label}.csv", sep=";"
            )

    return
