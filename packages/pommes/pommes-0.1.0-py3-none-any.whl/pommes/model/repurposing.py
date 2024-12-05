import linopy


def add_repurposing(model, model_parameters, annualised_totex_def, operation_adequacy_constraint):
    """
    Add variables and constraints related to repurposing to the Linopy model.

    Parameters
    ----------
    model : linopy.Model
        The Linopy Model object representing the energy system model.

    model_parameters : ModelParameters
        Model parameters from the build_model function.

    operation_adequacy_constraint : linopy.Constraint
        Linopy Constraint representing the total capacity constraint.

    Returns
    -------
    linopy.Model
        The updated Linopy Model object with added repurposing-related variables and constraints.
    """
    m = model
    p = model_parameters

    transInvest_Dvar = m.add_variables(
        name="transInvest_Dvar",
        lower=0,
        coords=[
            p.areas,
            p.years_inv,
            p.repurposing.tech_from,
            p.repurposing.tech_to,
        ],
        mask=p.repurposing.factor > 0,
    )

    # TODO: proper model for repurposing
    """    operation_adequacy_constraint.lhs += transInvest_Dvar.sum("tech_from").rename(
        {"tech_to": "conversion_tech", "year_inv": "year_op"}
    ) - transInvest_Dvar.sum("tech_to").rename(
        {"tech_from": "conversion_tech", "year_inv": "year_op"}
    )"""

    capacityCCSCtr = m.add_constraints(
        linopy.expressions.merge(
            [
                transInvest_Dvar.sel(tech_from="smr", tech_to="smr_ccs1") +
                # transInvest_Dvar.loc[:, :, "smr", "smr_ccs2"] -
                -1 * m.variables.planning_conversion_power_capacity.sel(conversion_tech="ccs1"),
                transInvest_Dvar.sel(tech_from=["smr", "smr_ccs1"], tech_to="smr_ccs2").sum(
                    "tech_from"
                )
                - m.variables.planning_conversion_power_capacity.sel(conversion_tech="ccs2"),
            ],
            dim="tech_to",
        )
        == 0,
        name="capacityCCSCtr",
    )  # TODO use the repurposing factor !

    # TransInvestCtr: filter on variable creation

    Transoperation_conversion_power_max_constraint = m.add_constraints(
        transInvest_Dvar.sum("tech_to").rename({"tech_from": "conversion_tech"})
        - m.variables.operation_conversion_power_capacity.rename({"year_op": "year_inv"})
        .sel(conversion_tech=p.repurposing.tech_from.values)
        .shift(year_inv=1)
        <= 0,
        name="Transoperation_conversion_power_max_constraint",
    )  # the shift automatically constrains at year_op = y0

    return m
