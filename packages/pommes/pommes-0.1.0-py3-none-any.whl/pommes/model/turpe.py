import linopy


def add_turpe(model, model_parameters, annualised_totex_def):
    """
    Add variables and constraints related to TURPE costs modelling (Tarif d'Utilisation des Réseaux
    Publics d'Électricité) to the Linopy model.

    Parameters
    ----------
    model : linopy.Model
        The Linopy Model object representing the energy system model.

    model_parameters : ModelParameters
                Model parameters from the build_model function.

    annualised_totex_def : linopy.model.Constraint
        The adequacy model constraint defining the annualised costs.

    Returns
    -------
    linopy.Model
        The updated Linopy Model object with added TURPE-related variables and constraints.
    """
    m = model
    p = model_parameters
    v = m.variables

    # ------------
    # Variables
    # ------------

    # Operation - TURPE

    operation_turpe_contract_power = m.add_variables(
        name="operation_turpe_contract_power",
        lower=0,
        coords=[p.area, p.hour_type, p.year_op],
    )
    # TODO: add differentiate contract power for injection ans withdrawal?

    # Costs - TURPE

    operation_turpe_variable_costs = m.add_variables(
        name="operation_turpe_variable_costs", lower=0, coords=[p.area, p.year_op]
    )

    operation_turpe_fixed_costs = m.add_variables(
        name="operation_turpe_fixed_costs", lower=0, coords=[p.area, p.year_op]
    )

    # ------------------
    # Objective function
    # ------------------

    annualised_totex_def.lhs += operation_turpe_variable_costs + operation_turpe_fixed_costs

    # --------------
    # Constraints
    # --------------

    # Operation - TURPE

    m.add_constraints(
        linopy.expressions.merge(
            [
                v.operation_net_import_abs.sel(resource="electricity").where(
                    p.turpe_calendar == hour_type
                )
                - operation_turpe_contract_power.sel(hour_type=hour_type)
                for hour_type in p.hour_type
            ],
            dim="hour_type",
        )
        <= 0,
        name="operation_turpe_contract_power_max_constraint",
    )

    m.add_constraints(
        operation_turpe_contract_power - operation_turpe_contract_power.shift(hour_type=1) >= 0,
        name="operation_turpe_increasing_contract_power_constraint",
    )

    # Costs - TURPE

    m.add_constraints(
        (
            linopy.expressions.merge(
                [
                    v.operation_net_import_abs.sel(resource="electricity").where(
                        p.turpe_calendar == hour_type
                    )
                    * p.turpe_variable_cost.sel(hour_type=hour_type)
                    for hour_type in p.hour_type
                ],
                dim="hour",
            )
            # *p.time_step_duration
            # TODO Check the issue with the index hour
            #  (here problem of dimension due to a broadcast of the index by the merge function)
        ).sum("hour")
        - operation_turpe_variable_costs
        == 0,
        name="operation_turpe_variable_costs_def",
    )

    m.add_constraints(
        (
            (operation_turpe_contract_power - operation_turpe_contract_power.shift(hour_type=1))
            * p.turpe_fixed_cost
        ).sum("hour_type")
        - operation_turpe_fixed_costs
        == 0,
        name="operation_turpe_fixed_costs_def",
    )

    return m
