import os
import warnings

import numpy as np
import pandas as pd
import xarray as xr
import xpress as xp
from linopy.solvers import (
    Result,
    Solution,
    Status,
    logger,
    maybe_adjust_objective_sign,
    maybe_convert_path,
    safe_get_solution,
    set_int_index,
)

print(f"Xpress version: {xp.getversion()}")


def run_xpress(
    xpress_problem,
    linopy_model,
    io_api="lp",
    log_fn=None,
    warmstart_fn=None,
    basis_fn=None,
    **solver_options,
):
    CONDITION_MAP = {
        "lp_optimal": "optimal",
        "mip_optimal": "optimal",
        "lp_infeasible": "infeasible",
        "lp_infeas": "infeasible",
        "mip_infeasible": "infeasible",
        "lp_unbounded": "unbounded",
        "mip_unbounded": "unbounded",
    }

    log_fn = maybe_convert_path(log_fn)
    warmstart_fn = maybe_convert_path(warmstart_fn)
    basis_fn = maybe_convert_path(basis_fn)

    xpress_problem.setControl(solver_options)

    if log_fn is not None:
        xpress_problem.setlogfile(log_fn)

    if warmstart_fn:
        xpress_problem.readbasis(warmstart_fn)

    xpress_problem.solve()

    if basis_fn:
        try:
            if os.path.isfile(f"temp/{basis_fn}"):
                warnings.warn(f"File 'temp/{basis_fn}' exists and will be overridden")
            xpress_problem.writebasis(basis_fn)
        except Exception as err:
            logger.info("No model basis stored. Raised error: %s", err)

    condition = xpress_problem.getProbStatusString()
    termination_condition = CONDITION_MAP.get(condition, condition)
    status = Status.from_termination_condition(termination_condition)
    status.legacy_status = condition

    def get_solver_solution() -> Solution:
        objective = xpress_problem.getObjVal()

        var = [str(v) for v in xpress_problem.getVariable()]

        sol = pd.Series(xpress_problem.getSolution(var), index=var, dtype=float)
        sol = set_int_index(sol)

        try:
            dual = [str(d) for d in xpress_problem.getConstraint()]
            dual = pd.Series(xpress_problem.getDual(dual), index=dual, dtype=float)
            dual = set_int_index(dual)
        except xp.SolverError:
            logger.warning("Dual values of MILP couldn't be parsed")
            dual = pd.Series(dtype=float)

        return Solution(sol, dual, objective)

    solution = safe_get_solution(status, get_solver_solution)
    maybe_adjust_objective_sign(solution, linopy_model.objective.sense, io_api)

    return Result(status, solution, xpress_problem)


def export_xpress_solution_to_linopy(result, model):
    result.info()

    model.objective._value = result.solution.objective
    model.status = result.status.status.value
    model.termination_condition = result.status.termination_condition.value
    model.solver_model = result.solver_model

    if not result.status.is_ok:
        return result.status.status.value, result.status.termination_condition.value

    # map solution and dual to original shape which includes missing values
    sol = result.solution.primal.copy()
    sol.loc[-1] = np.nan

    for name, var in model.variables.items():
        idx = np.ravel(var.labels)
        try:
            vals = sol[idx].values.reshape(var.labels.shape)
        except KeyError:
            vals = sol.reindex(idx).values.reshape(var.labels.shape)
        var.solution = xr.DataArray(vals, var.coords)

    if not result.solution.dual.empty:
        dual = result.solution.dual.copy()
        dual.loc[-1] = np.nan

        for name, con in model.constraints.items():
            idx = np.ravel(con.labels)
            try:
                vals = dual[idx].values.reshape(con.labels.shape)
            except KeyError:
                vals = dual.reindex(idx).values.reshape(con.labels.shape)
            con.dual = xr.DataArray(vals, con.labels.coords)

    return result.status.status.value, result.status.termination_condition.value


def update_xpress_problem(model, problem, update, copy=True):
    if copy:
        p = problem.copy()
    else:
        p = problem

    list_constraints = []
    list_variables = []
    list_coefficients = []

    for constraint, constraint_param in update.items():
        constraint_label = (
            f"c{int(model.constraints[constraint].sel(constraint_param['coords']).labels)}"
        )
        for variable, variable_param in constraint_param["variables"].items():
            variable_label = (
                f"x{int(model.variables[variable].sel(variable_param['coords']).labels)}"
            )
            coefficient = variable_param["coefficient"]

            list_constraints.append(constraint_label)
            list_variables.append(variable_label)
            list_coefficients.append(coefficient)

    p.chgmcoef(list_constraints, list_variables, list_coefficients)

    return p
