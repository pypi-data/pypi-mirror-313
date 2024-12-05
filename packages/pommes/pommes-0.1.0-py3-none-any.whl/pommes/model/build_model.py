import numpy as np
from linopy import Model

from pommes.model.carbon import add_carbon
from pommes.model.combined import add_combined
from pommes.model.conversion import add_conversion
from pommes.model.net_import import add_net_import
from pommes.model.storage import add_storage
from pommes.model.transport import add_transport
from pommes.model.turpe import add_turpe


def build_model(model_parameters):
    """
    Build a Linopy Model based on the provided model parameters.

    Args:
        model_parameters (xarray.Dataset):
            Model parameters containing information about the energy system.
            The dataset is built in the `build_input_dataset` function. The structure is described below.

    Returns:
        Model:
            Linopy Model object representing the energy system model.

    Examples:
        The xarray Dataset `model_parameters` must have the following core indexes:

        - **Area (`area`)**: str
          Represents the different geographical areas covered by the model.
        - **Hour (`hour`)**: int64
          Time index representing different hours for which the model is evaluated.
        - **Resource (`resource`)**: str
          Different types of resources, such as renewable or non-renewable energy.
        - **Year of Decision (`year_dec`)**: int64
          The year in which the decision is made.
        - **Year of Investment (`year_inv`)**: int64
          The year when an investment takes place.
        - **Year of Operation (`year_op`)**: int64
          The year in which the operation occurs.

        Depending on the present assets, the following additional indexes may be required for specific modules:

        - **Conversion Module**:
            - **Conversion Technology (`conversion_tech`)**: str
              Specifies the type of conversion technology being used, such as a gas turbine or wind turbine.

        - **Combined Module**:
            - **Combined Technology (`combined_tech`)**: str
              Specifies the combined technology being used.
            - **Mode (`mode`)**: str
              Represents different operating modes of the combined technology.

        - **Storage Module**:
            - **Storage Technology (`storage_tech`)**: str
              Represents the type of storage technology, such as batteries or pumped hydro storage.

        - **Transport Module**:
            - **Link (`link`)**: str
              Represents the connections between areas.
            - **Transport Technology (`transport_tech`)**: str
              Specifies the type of transport technology, such as power lines or gas pipelines.

        - **Turpe Module**:
            - **Hour Type (`hour_type`)**: str
              Represents different types of hours, such as peak or off-peak.

        Data variables are described in the `pommes/dataset_description.yaml` file.

        The `check_inputs` function from the `pommes.io.build_input_dataset` module ensures data consistency.
    """

    p = model_parameters

    operation_year_normalization = p.operation_year_duration / p.time_step_duration.sum("hour")

    m = Model()

    # ------------
    # Variables
    # ------------

    # Operation - load_shedding & spillage

    operation_load_shedding = m.add_variables(
        name="operation_load_shedding",
        lower=0,
        mask=np.logical_or(
            np.isnan(p.load_shedding_max_capacity),
            p.load_shedding_max_capacity > 0,
        ),
        coords=[p.area, p.hour, p.resource, p.year_op],
    )

    operation_spillage = m.add_variables(
        name="operation_spillage",
        lower=0,
        mask=np.logical_or(
            np.isnan(p.spillage_max_capacity),
            p.spillage_max_capacity > 0,
        ),
        coords=[p.area, p.hour, p.resource, p.year_op],
    )

    # Costs - load_shedding & spillage

    operation_load_shedding_costs = m.add_variables(
        name="operation_load_shedding_costs",
        coords=[p.area, p.year_op],
    )

    operation_spillage_costs = m.add_variables(
        name="operation_spillage_costs",
        coords=[p.area, p.year_op],
    )

    # Annualised costs

    annualised_totex = m.add_variables(name="annualised_totex", coords=[p.area, p.year_op])

    # ------------------
    # Objective function
    # ------------------

    m.add_objective(p.discount_factor * annualised_totex.sum("area"))

    # --------------
    # Constraints
    # --------------

    # Adequacy constraint

    operation_adequacy_constraint = m.add_constraints(
        operation_load_shedding - operation_spillage - p.demand == 0,
        name="operation_adequacy_constraint",
    )

    # Operation - load_shedding & spillage

    m.add_constraints(
        operation_load_shedding <= p.load_shedding_max_capacity,
        mask=np.isfinite(p.load_shedding_max_capacity) * (p.load_shedding_max_capacity > 0),
        name="operation_load_shedding_max_constraint",
    )

    m.add_constraints(
        operation_spillage <= p.spillage_max_capacity,
        mask=np.isfinite(p.spillage_max_capacity) * (p.spillage_max_capacity > 0),
        name="operation_spillage_max_constraint",
    )

    # Costs - load_shedding & spillage

    m.add_constraints(
        -operation_load_shedding_costs
        + (operation_load_shedding.sum(["hour"]) * p.load_shedding_cost).sum(["resource"])
        * operation_year_normalization
        == 0,
        name="operation_load_shedding_costs_def",
    )

    m.add_constraints(
        -operation_spillage_costs
        + (operation_spillage.sum(["hour"]) * p.spillage_cost).sum(["resource"])
        * operation_year_normalization
        == 0,
        name="operation_spillage_costs_def",
    )
    # Annualised costs

    annualised_totex_def = m.add_constraints(
        -annualised_totex + operation_load_shedding_costs + operation_spillage_costs == 0,
        name="annualised_totex_def",
    )

    # -----------------------------------------
    # Other sets of variables and constraints
    # -----------------------------------------

    if "conversion" in p.keys() and p.conversion:
        m = add_conversion(
            m, p, annualised_totex_def, operation_year_normalization, operation_adequacy_constraint
        )

    if "storage" in p.keys() and p.storage:
        m = add_storage(m, p, annualised_totex_def, operation_adequacy_constraint)

    if "transport" in p.keys() and p.transport:
        m = add_transport(m, p, annualised_totex_def, operation_adequacy_constraint)

    if "combined" in p.keys() and p.conversion:
        m = add_combined(
            m, p, annualised_totex_def, operation_year_normalization, operation_adequacy_constraint
        )

    # if p.repurposing is not None:
    #     m = add_repurposing(m, p, annualised_totex_def, operation_adequacy_constraint)

    if "net_import" in p.keys() and p.net_import:
        m = add_net_import(
            m, p, annualised_totex_def, operation_year_normalization, operation_adequacy_constraint
        )

    if "carbon" in p.keys() and p.carbon:
        m = add_carbon(m, p, annualised_totex_def, operation_year_normalization)

    if "turpe" in p.keys() and p.turpe:
        m = add_turpe(m, p, annualised_totex_def)

    return m
