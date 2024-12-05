import numpy as np
import xarray as xr


def add_storage(
    model,
    model_parameters,
    annualised_totex_def,
    operation_adequacy_constraint,
):
    """
    Add storage-related variables, constraints, and objective to the Linopy model.

    Parameters
    ----------
    model : linopy.Model
        The Linopy Model object representing the energy system model.

    model_parameters : ModelParameters
        Model parameters from the build_model function.

    annualised_totex_def : linopy.model.Constraint
        The adequacy model constraint defining the annualised costs.

    operation_adequacy_constraint : linopy.model.Constraint
        Linopy Constraint representing the adequacy constraint for abstract models.

    Returns
    -------
    linopy.Model
        The updated Linopy Model object with added storage-related variables, constraints, and objective.
    """
    m = model
    p = model_parameters

    # ------------
    # Variables
    # ------------

    # Operation - Storage

    operation_storage_energy_capacity = m.add_variables(
        name="operation_storage_energy_capacity",
        lower=0,
        coords=[p.area, p.storage_tech, p.year_op],
    )

    operation_storage_power_capacity = m.add_variables(
        name="operation_storage_power_capacity",
        lower=0,
        coords=[p.area, p.storage_tech, p.year_op],
        # TODO: Variable P_in and P_out power?
    )

    operation_storage_level = m.add_variables(
        name="operation_storage_level",
        lower=0,
        coords=[p.area, p.hour, p.storage_tech, p.year_op],
    )

    operation_storage_power_in = m.add_variables(
        name="operation_storage_power_in",
        lower=0,
        coords=[p.area, p.hour, p.storage_tech, p.year_op],
    )

    operation_storage_power_out = m.add_variables(
        name="operation_storage_power_out",
        lower=0,
        coords=[p.area, p.hour, p.storage_tech, p.year_op],
    )

    # Operation - Storage intermediate variables

    operation_storage_net_generation = m.add_variables(
        name="operation_storage_net_generation",
        coords=[p.area, p.hour, p.storage_tech, p.resource, p.year_op],
        mask=np.isfinite(p.storage_factor_in) * (p.storage_factor_in != 0)
        + np.isfinite(p.storage_factor_out) * (p.storage_factor_out != 0)
        + np.isfinite(p.storage_factor_keep) * (p.storage_factor_keep != 0)
        > 0,
    )

    # Planning - Storage

    planning_storage_energy_capacity = m.add_variables(
        name="planning_storage_energy_capacity",
        lower=0,
        coords=[p.area, p.storage_tech, p.year_dec, p.year_inv],
        mask=xr.where(
            cond=p.storage_early_decommissioning,
            x=(p.year_inv < p.year_dec)
            * (p.year_dec <= p.storage_end_of_life)
            * np.logical_or(
                p.year_dec <= p.year_inv.max(),
                p.year_dec == p.storage_end_of_life,
            ),
            y=p.year_dec == p.storage_end_of_life,
        ),
    )

    planning_storage_power_capacity = m.add_variables(
        name="planning_storage_power_capacity",
        lower=0,
        coords=[p.area, p.storage_tech, p.year_dec, p.year_inv],
        mask=xr.where(
            cond=p.storage_early_decommissioning,
            x=(p.year_inv < p.year_dec)
            * (p.year_dec <= p.storage_end_of_life)
            * np.logical_or(
                p.year_dec <= p.year_inv.max(),
                p.year_dec == p.storage_end_of_life,
            ),
            y=p.year_dec == p.storage_end_of_life,
        ),
    )

    # Costs - Storage

    operation_storage_costs = m.add_variables(
        name="operation_storage_costs", lower=0, coords=[p.area, p.storage_tech, p.year_op]
    )

    planning_storage_costs = m.add_variables(
        name="planning_storage_costs", lower=0, coords=[p.area, p.storage_tech, p.year_op]
    )

    # ------------------
    # Objective function
    # ------------------

    annualised_totex_def.lhs += operation_storage_costs.sum(
        "storage_tech"
    ) + planning_storage_costs.sum("storage_tech")

    # --------------
    # Constraints
    # --------------

    # Adequacy constraint

    operation_adequacy_constraint.lhs += operation_storage_net_generation.sum("storage_tech")

    # Operation - Storage

    m.add_constraints(
        -operation_storage_level
        # It is assumed that the storage dissipation is defined per hour
        + operation_storage_level.roll(hour=1) * (1 - p.storage_dissipation) ** p.time_step_duration
        + (operation_storage_power_in - operation_storage_power_out) * p.time_step_duration
        == 0,
        name="operation_storage_level_def",
    )

    m.add_constraints(
        operation_storage_power_in - operation_storage_power_capacity <= 0,
        name="operation_storage_power_in_max_constraint",
    )

    m.add_constraints(
        operation_storage_power_out - operation_storage_power_capacity <= 0,
        name="operation_storage_power_out_max_constraint",
    )

    m.add_constraints(
        operation_storage_level - operation_storage_energy_capacity <= 0,
        name="operation_storage_level_max_constraint",
    )

    # Operation - Storage intermediate variables

    m.add_constraints(
        -operation_storage_power_capacity
        + planning_storage_power_capacity.where(
            (p.year_inv <= p.year_op) * (p.year_op < p.year_dec)
        ).sum(["year_dec", "year_inv"])
        == 0,
        name="operation_storage_power_capacity_def",
    )

    m.add_constraints(
        -operation_storage_energy_capacity
        + planning_storage_energy_capacity.where(
            (p.year_inv <= p.year_op) * (p.year_op < p.year_dec)
        ).sum(["year_dec", "year_inv"])
        == 0,
        name="operation_storage_energy_capacity_def",
    )

    m.add_constraints(
        -operation_storage_net_generation
        + p.time_step_duration
        * (
            operation_storage_power_in * p.storage_factor_in
            + operation_storage_level * p.storage_factor_keep
            + operation_storage_power_out * p.storage_factor_out
        )
        == 0,
        name="operation_storage_net_generation_def",
        mask=np.isfinite(p.storage_factor_in) * (p.storage_factor_in != 0)
        + np.isfinite(p.storage_factor_out) * (p.storage_factor_out != 0)
        + np.isfinite(p.storage_factor_keep) * (p.storage_factor_keep != 0)
        > 0,
    )

    # Planning - Storage

    m.add_constraints(
        planning_storage_power_capacity.sum("year_dec") >= p.storage_power_capacity_investment_min,
        name="planning_storage_power_capacity_min_constraint",
        mask=np.isfinite(p.storage_power_capacity_investment_min)
        * np.not_equal(
            p.storage_power_capacity_investment_min, p.storage_power_capacity_investment_max
        ),
    )

    m.add_constraints(
        planning_storage_power_capacity.sum("year_dec") <= p.storage_power_capacity_investment_max,
        name="planning_storage_power_capacity_max_constraint",
        mask=np.isfinite(p.storage_power_capacity_investment_max)
        * np.not_equal(
            p.storage_power_capacity_investment_min, p.storage_power_capacity_investment_max
        ),
    )

    m.add_constraints(
        planning_storage_power_capacity.sum("year_dec") == p.storage_power_capacity_investment_max,
        name="planning_storage_power_capacity_def",
        mask=np.isfinite(p.storage_power_capacity_investment_max)
        * np.equal(
            p.storage_power_capacity_investment_min, p.storage_power_capacity_investment_max
        ),
    )

    m.add_constraints(
        planning_storage_energy_capacity.sum("year_dec")
        >= p.storage_energy_capacity_investment_min,
        name="planning_storage_energy_capacity_min_constraint",
        mask=np.isfinite(p.storage_energy_capacity_investment_min)
        * np.not_equal(
            p.storage_energy_capacity_investment_min, p.storage_energy_capacity_investment_max
        ),
    )

    m.add_constraints(
        planning_storage_energy_capacity.sum("year_dec")
        <= p.storage_energy_capacity_investment_max,
        name="planning_storage_energy_capacity_max_constraint",
        mask=np.isfinite(p.storage_energy_capacity_investment_max)
        * np.not_equal(
            p.storage_energy_capacity_investment_min, p.storage_energy_capacity_investment_max
        ),
    )

    m.add_constraints(
        planning_storage_energy_capacity.sum("year_dec")
        == p.storage_energy_capacity_investment_max,
        name="planning_storage_energy_capacity_def",
        mask=np.isfinite(p.storage_energy_capacity_investment_max)
        * np.equal(
            p.storage_energy_capacity_investment_min, p.storage_energy_capacity_investment_max
        ),
    )

    # Costs - Storage

    m.add_constraints(
        -operation_storage_costs
        # No variable costs in the model for storage
        + (p.storage_fixed_cost_power * operation_storage_power_capacity)
        + (p.storage_fixed_cost_energy * operation_storage_energy_capacity)
        == 0,
        name="operation_storage_costs_def",
    )

    m.add_constraints(
        -planning_storage_costs
        + (
            (
                planning_storage_power_capacity * p.storage_annuity_cost_power
                + planning_storage_energy_capacity * p.storage_annuity_cost_energy
            )
            .where((p.year_inv <= p.year_op) * (p.year_op < p.year_dec))
            .sum(["year_dec", "year_inv"])
        ).where(
            cond=p.storage_annuity_perfect_foresight,
            other=(
                (
                    planning_storage_power_capacity.sum("year_dec")
                    * p.storage_annuity_cost_power.min(
                        [dim for dim in p.storage_annuity_cost_power.dims if dim == "year_dec"]
                    )
                    + planning_storage_energy_capacity.sum("year_dec")
                    * p.storage_annuity_cost_energy.min(
                        [dim for dim in p.storage_annuity_cost_energy.dims if dim == "year_dec"]
                    )
                )
                .where((p.year_inv <= p.year_op) * (p.year_op < p.storage_end_of_life))
                .sum(["year_inv"])
            ),
        )
        == 0,
        name="planning_storage_costs_def",
    )

    return m
