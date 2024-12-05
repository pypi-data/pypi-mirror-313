import numpy as np
import xarray as xr


def add_carbon(model, model_parameters, annualised_totex_def, operation_year_normalization):
    """
    Add carbon-related variables, constraints, and objective terms to the energy system model.

    Parameters
    ----------
    model : linopy.Model
        The Linopy Model object representing the energy system model.

    model_parameters : ModelParameters
        Model parameters from the build_model function.

    annualised_totex_def : linopy.model.Constraint
        The adequacy model constraint defining the annualised costs.

    operation_year_normalization : float
        Normalize the total duration of the operations modelled per operation year by the number of hours in a year

    Returns
    -------
    linopy.Model
        The updated Linopy Model object with carbon-related variables, constraints, and objective terms.
    """
    m = model
    p = model_parameters
    v = m.variables

    # ------------
    # Variables
    # ------------

    # Operation - Carbon

    operation_carbon_emissions = m.add_variables(
        name="operation_carbon_emissions", coords=[p.area, p.hour, p.year_op]
    )

    operation_total_carbon_emissions = m.add_variables(
        name="operation_total_carbon_emissions", coords=[p.area, p.hour, p.year_op]
    )

    # Costs - Carbon

    operation_carbon_costs = m.add_variables(
        name="operation_carbon_costs", lower=0, coords=[p.area, p.year_op]
    )

    # ------------------
    # Objective function
    # ------------------

    annualised_totex_def.lhs += operation_carbon_costs

    # --------------
    # Constraints
    # --------------

    # Operation - Carbon

    m.add_constraints(
        # Warning, timestep_duration is used here and for the total emission as there is a "duplication"
        # of the variables operation_total_carbon_emissions and operation_carbon_emissions
        +operation_year_normalization * operation_total_carbon_emissions.sum(["area", "hour"])
        <= p.carbon_goal,
        mask=np.isfinite(p.carbon_goal),
        name="operation_carbon_goal_constraint",
    )

    # Operation - Carbon intermediate variables

    operation_carbon_emissions_def = m.add_constraints(
        -operation_carbon_emissions
        + (v.operation_conversion_power * p.conversion_emission_factor).sum(["conversion_tech"])
        * p.time_step_duration
        == 0,
        name="operation_carbon_emissions_def",
    )

    operation_total_carbon_emissions_def = m.add_constraints(
        -operation_total_carbon_emissions
        + (v.operation_conversion_power * p.conversion_emission_factor).sum(["conversion_tech"])
        * p.time_step_duration
        == 0,
        name="operation_total_carbon_emissions_def",
    )

    if "net_import" in p.keys():
        operation_carbon_emissions_def.lhs += (
            v.operation_net_import_import * p.net_import_emission_factor
        ).sum(["resource"]) * p.time_step_duration
        operation_total_carbon_emissions_def.lhs += (
            v.operation_net_import_import * p.net_import_total_emission_factor
        ).sum(["resource"]) * p.time_step_duration

    # Costs - Carbon

    m.add_constraints(
        -operation_carbon_costs
        # Warning, timestep_duration is used here and for the total costs as there is a "duplication"
        # of the variables operation_total_carbon_emissions and operation_carbon_emissions
        + operation_year_normalization
        * operation_carbon_emissions.sum("hour")
        * xr.where(
            cond=np.isfinite(p.carbon_tax),
            x=p.carbon_tax,
            y=0,
        )
        == 0,
        name="operation_carbon_costs_def",
    )

    return m
