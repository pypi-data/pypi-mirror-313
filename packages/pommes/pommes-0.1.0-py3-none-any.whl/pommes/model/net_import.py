import numpy as np


def add_net_import(
    model,
    model_parameters,
    annualised_totex_def,
    operation_year_normalization,
    operation_adequacy_constraint,
):
    """
    Add variables, constraints, and objective terms related to energy net imports from the rest of the world (ROW)
    to the model.

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

    operation_adequacy_constraint : linopy.model.Constraint
        The Linopy Constraint representing the adequacy in the model.

    Returns
    -------
    linopy.Model
        The updated Linopy Model object with variables, constraints, and objective terms related to energy
        net imports with the rest of the world.
    """
    m = model
    p = model_parameters

    # ------------
    # Variables
    # ------------

    # Operation - Imports & exports from rest of the world

    operation_net_import_import = m.add_variables(
        name="operation_net_import_import",
        lower=0,
        coords=[p.area, p.hour, p.resource, p.year_op],
    )

    operation_net_import_export = m.add_variables(
        name="operation_net_import_export",
        lower=0,
        coords=[p.area, p.hour, p.resource, p.year_op],
    )

    # Operation - Imports & exports intermediate variables

    operation_net_import_abs = m.add_variables(
        name="operation_net_import_abs",
        lower=0,
        coords=[p.area, p.hour, p.resource, p.year_op],
    )

    operation_net_import_net_generation = m.add_variables(
        name="operation_net_import_net_generation",
        coords=[p.area, p.hour, p.resource, p.year_op],
    )

    # Costs - Imports & exports

    operation_net_import_costs = m.add_variables(
        name="operation_net_import_costs", coords=[p.area, p.resource, p.year_op]
    )

    # ------------------
    # Objective function
    # ------------------

    annualised_totex_def.lhs += operation_net_import_costs.sum("resource")

    # --------------
    # Constraints
    # --------------

    # Adequacy constraint

    operation_adequacy_constraint.lhs += operation_net_import_net_generation

    # Operation - Imports & exports

    # TODO: add max power constraint on transports with ROW

    # Operation - Imports & exports other constraints

    m.add_constraints(
        operation_year_normalization * operation_net_import_import.sum(["area", "hour"])
        <= p.net_import_max_yearly_energy_import,
        mask=np.isfinite(p.net_import_max_yearly_energy_import),
        name="operation_net_import_import_yearly_max_constraint",
    )

    m.add_constraints(
        operation_year_normalization * operation_net_import_export.sum(["area", "hour"])
        <= p.net_import_max_yearly_energy_export,
        mask=np.isfinite(p.net_import_max_yearly_energy_export),
        name="operation_net_import_export_yearly_max_constraint",
    )

    # Operation - Imports & exports intermediate variables

    m.add_constraints(
        -operation_net_import_abs + operation_net_import_import + operation_net_import_export == 0,
        name="operation_net_import_abs_def",
    )

    m.add_constraints(
        -operation_net_import_net_generation
        + operation_net_import_import
        - operation_net_import_export
        == 0,
        name="operation_net_import_net_generation_def",
    )

    # Costs - Imports & exports

    m.add_constraints(
        -operation_net_import_costs
        # Normalised variable cots with the duration of the operation periods to be consistent with annualised costs
        + operation_year_normalization
        * (
            +p.net_import_import_price * operation_net_import_import
            - p.net_import_export_price * operation_net_import_export
        ).sum("hour")
        == 0,
        name="operation_net_import_costs_def",
    )

    return m
