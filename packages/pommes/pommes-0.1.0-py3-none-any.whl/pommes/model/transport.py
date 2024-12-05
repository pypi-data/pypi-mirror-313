import numpy as np
import xarray as xr


def add_transport(
    model,
    model_parameters,
    annualised_totex_def,
    operation_adequacy_constraint,
):
    """
    Add transport-related components to the Linopy model, including variables, costs, and constraints.

    Args:
        model (Linopy.Model):
            The Linopy model to which transport-related elements will be added.
        model_parameters (xarray.Dataset):
            Dataset containing energy system parameters.
        annualised_totex_def (Linopy.Expression):
            Expression representing the annualised total expenditure (totex), which will be updated with transport-specific costs.
        time_step (float):
            The time step duration used to scale time-based constraints, such as power flow limits.
        operation_adequacy_constraint (Linopy.Expression):
            Expression representing operational adequacy, which ensures supply meets demand. This will be updated with transport-related contributions.

    Returns:
        Linopy.Model:
            The model updated with transport-related variables, costs, and constraints.

    **Note**:

    This function introduces the following elements into the model:

    **Variables**

    - *Operation*
        - ``operation_transport_power_capacity``
            Represents the operational power capacity for each transport technology by link and operational year.
        - ``operation_transport_power``
            Represents the operational power flow for each transport technology by link, hour, and operational year.

        - *Intermediate variables*
            - ``operation_transport_net_generation``
                Represents the net generation from transport technologies, calculated for each area, technology, hour, resource, and operational year.

    - *Planning*
        - ``planning_transport_power_capacity``
            Represents the planned power capacity for each transport technology by link, decision year, and investment year.

    - *Costs (intermediate variables)*:
        - ``operation_transport_costs``
            Represents the operational costs associated with transport technologies for each area, technology, and operational year.
        - ``planning_transport_costs``
            Represents the planning costs associated with transport technologies for each area, technology, and operational year.

    **Constraints**

    - *Operation*
        - ``operation_transport_power_max_constraint``
            Limits operational power to the available power capacity for each transport technology.

        - *Operational capacity*
            - ``operation_transport_power_capacity_def``
                Defines the operational power capacity based on the planned investments over the years.

        - *Intermediate variables definition*
            - ``operation_transport_net_generation_def``
                Relates net generation to power flows between areas, ensuring consistent accounting.

    - *Planning*
        - ``planning_transport_power_capacity_min_constraint``
            Sets a lower limit on planned power capacity investments for transport technologies.
        - ``planning_transport_power_capacity_max_constraint``
            Sets an upper limit on planned power capacity investments for transport technologies.
        - ``planning_transport_power_capacity_def``
            Ensures planned power capacity matches the minimum requirement when upper and lower limits are equal.

    - *Costs*
        - ``operation_transport_costs_def``
            Defines operational costs as a function of fixed costs and power capacity for transport technologies.
        - ``planning_transport_costs_def``
            Defines planning costs, accounting for investment costs spread over operational periods, with optional perfect foresight.

    These additions ensure that the transport technologies operate within feasible and efficient limits, respecting capacity constraints and power flow capabilities. The model is thereby enhanced to accurately simulate transport behavior and costs.
    """
    m = model
    p = model_parameters

    # ------------
    # Variables
    # ------------

    # Operation - transport

    operation_transport_power_capacity = m.add_variables(
        name="operation_transport_power_capacity",
        lower=0,
        coords=[p.link, p.transport_tech, p.year_op],
    )

    operation_transport_power = m.add_variables(
        name="operation_transport_power",
        lower=0,
        coords=[p.link, p.transport_tech, p.hour, p.year_op],
    )

    # Operation - transport intermediate variables

    operation_transport_net_generation = m.add_variables(
        name="operation_transport_net_generation",
        coords=[p.area, p.hour, p.transport_tech, p.resource, p.year_op],
        mask=(p.transport_resource == p.resource).any(
            [dim for dim in ["link"] if dim in p.transport_resource.dims]
        ),
    )

    # Planning - transport

    planning_transport_power_capacity = m.add_variables(
        name="planning_transport_power_capacity",
        lower=0,
        coords=[p.link, p.transport_tech, p.year_dec, p.year_inv],
        mask=xr.where(
            cond=p.transport_early_decommissioning,
            x=(p.year_inv < p.year_dec)
            * (p.year_dec <= p.transport_end_of_life)
            * np.logical_or(
                p.year_dec <= p.year_inv.max(),
                p.year_dec == p.transport_end_of_life,
            ),
            y=p.year_dec == p.transport_end_of_life,
        ),
    )

    # Costs - transport

    operation_transport_costs = m.add_variables(
        name="operation_transport_costs",
        lower=0,
        coords=[p.area, p.transport_tech, p.year_op],
    )

    planning_transport_costs = m.add_variables(
        name="planning_transport_costs",
        lower=0,
        coords=[p.area, p.transport_tech, p.year_op],
    )

    # ------------------
    # Objective function
    # ------------------

    m.objective += operation_transport_power * p.transport_hurdle_costs
    annualised_totex_def.lhs += (operation_transport_costs + planning_transport_costs).sum(
        ["transport_tech"]
    )

    # --------------
    # Constraints
    # --------------

    # Adequacy constraint

    operation_adequacy_constraint.lhs += operation_transport_net_generation.sum(["transport_tech"])

    # Operation - transport

    m.add_constraints(
        operation_transport_power - operation_transport_power_capacity <= 0,
        name="operation_transport_power_max_constraint",
    )

    # Operation - transport intermediate variables

    m.add_constraints(
        -operation_transport_power_capacity
        + planning_transport_power_capacity.where(
            (p.year_inv <= p.year_op) * (p.year_op < p.year_dec)
        ).sum(["year_dec", "year_inv"])
        == 0,
        name="operation_transport_power_capacity_def",
    )

    m.add_constraints(
        -operation_transport_net_generation
        + p.time_step_duration
        * (
            operation_transport_power.where(p.area == p.transport_area_to).sum("link")
            - operation_transport_power.where(p.area == p.transport_area_from).sum("link")
        ).where(
            (p.transport_resource == p.resource).any(
                [dim for dim in ["link", "year_inv"] if dim in p.transport_resource.dims]
            )
        )
        == 0,
        name="operation_transport_net_generation_def",
        mask=(p.transport_resource == p.resource).any(
            [dim for dim in ["link"] if dim in p.transport_resource.dims]
        ),
    )

    # Planning - transport

    m.add_constraints(
        planning_transport_power_capacity.sum("year_dec")
        >= p.transport_power_capacity_investment_min,
        name="planning_transport_power_capacity_min_constraint",
        mask=np.isfinite(p.transport_power_capacity_investment_min)
        * np.not_equal(
            p.transport_power_capacity_investment_min,
            p.transport_power_capacity_investment_max,
        ),
    )

    m.add_constraints(
        planning_transport_power_capacity.sum("year_dec")
        <= p.transport_power_capacity_investment_max,
        name="planning_transport_power_capacity_max_constraint",
        mask=np.isfinite(p.transport_power_capacity_investment_max)
        * np.not_equal(
            p.transport_power_capacity_investment_min,
            p.transport_power_capacity_investment_max,
        ),
    )

    m.add_constraints(
        planning_transport_power_capacity.sum("year_dec")
        == p.transport_power_capacity_investment_min,
        name="planning_transport_power_capacity_def",
        mask=np.isfinite(p.transport_power_capacity_investment_max)
        * np.equal(
            p.transport_power_capacity_investment_min,
            p.transport_power_capacity_investment_max,
        ),
    )

    # Costs - transport

    m.add_constraints(
        -operation_transport_costs
        # No variable costs in the model for transport
        + 0.5
        * (
            (p.transport_fixed_cost * operation_transport_power_capacity)
            .where(np.logical_or(p.area == p.transport_area_from, p.area == p.transport_area_to))
            .sum("link")
        )
        == 0,
        name="operation_transport_costs_def",
    )

    m.add_constraints(
        -planning_transport_costs
        + 0.5
        * (
            (p.transport_annuity_cost * planning_transport_power_capacity).where(
                np.logical_or(p.area == p.transport_area_from, p.area == p.transport_area_to)
            )
        )
        .sum(["link"])
        .where((p.year_inv <= p.year_op) * (p.year_op < p.year_dec))
        .sum(["year_dec", "year_inv"])
        .where(
            cond=p.transport_annuity_perfect_foresight,
            other=(
                (
                    (
                        planning_transport_power_capacity.sum("year_dec")
                        * p.transport_annuity_cost.min(
                            [dim for dim in ["year_dec"] if dim in p.transport_annuity_cost.dims]
                        )
                    ).where(
                        np.logical_or(
                            p.area == p.transport_area_from, p.area == p.transport_area_to
                        )
                    )
                )
                .where((p.year_inv <= p.year_op) * (p.year_op < p.transport_end_of_life))
                .sum(["link", "year_inv"])
            ),
        )
        == 0,
        name="planning_transport_costs_def",
    )

    return m
