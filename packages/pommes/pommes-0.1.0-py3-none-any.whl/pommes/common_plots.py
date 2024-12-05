import os

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import plotly.graph_objects as go
import xarray as xr
from plotly.subplots import make_subplots

from pommes.utils import array_to_datetime, get_main_resource


def generate_color_set(size, color_scale_name="Rainbow"):
    color_scale = getattr(pc.sequential, color_scale_name)
    return pc.sample_colorscale(color_scale, [i / (size - 1) for i in range(size)])


def save_plot(output_folder, name, dpi=300, show=True):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    plt.savefig(f"{output_folder}/{name}.png", dpi=dpi)
    if show:
        plt.show(block=True)


def plot_power(model_solution, plot_folder, plot_name="power"):
    fig = px.line(
        data_frame=model_solution.operation_conversion_power.to_series().reset_index(),
        x="hour",
        y="operation_conversion_power",
        color="conversion_tech",
    )

    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)
    fig.write_html(f"{plot_folder}/{plot_name}.html")
    return fig


def plot_energy_balance(
    model_parameters,
    model_solution,
    plot_folder,
    x_axis=None,
    facet_row=None,
    facet_col=None,
    plot_name="energy_balance",
    threshold=1e-6,
    showlegend=False,
):
    # TODO: avoid sum on year_invest
    s = model_solution
    p = model_parameters

    # ----------------
    # Data formatting
    # ----------------

    demand = (-1 * p.demand).expand_dims(category=["demand"])
    load_shedding = s.operation_load_shedding.expand_dims(category=["load_shedding"])
    spillage = (-1 * s.operation_spillage).expand_dims(category=["spillage"])
    conversion = s.operation_conversion_net_generation.rename(dict(conversion_tech="category"))
    combined = xr.DataArray([], coords=dict(category=[]))
    storage = xr.DataArray([], coords=dict(category=[]))
    net_import = xr.DataArray([], coords=dict(category=[]))
    transport = xr.DataArray([], coords=dict(category=[]))

    if "combined" in p.keys() and p.combined.any():
        combined = s.operation_combined_net_generation.rename(dict(combined_tech="category"))
    if "storage" in p.keys() and p.storage.any():
        storage = s.operation_storage_net_generation.rename(dict(storage_tech="category"))
    if "net_import" in p.keys() and p.net_import.any():
        net_import = s.operation_net_import_net_generation.expand_dims(category=["net_import"])
    if "transport" in p.keys() and p.transport.any():
        transport = s.operation_transport_net_generation.rename(dict(transport_tech="category"))

    da = xr.concat(
        [demand, load_shedding, spillage, combined, conversion, storage, net_import, transport],
        dim="category",
        coords="all",
        join="outer",
        compat="broadcast_equals",
    )

    if len(da.category) > 24:
        color_set = generate_color_set(len(da.category))
    else:
        color_set = pc.qualitative.Dark24

    color_map = {category: color_set[i] for i, category in enumerate(da.category.values)}

    if x_axis is None:
        x_axis = da.hour

    da = da.sum(
        [dim for dim in da.dims if dim not in [facet_row, facet_col, x_axis.dims[0], "category"]]
    )

    # ----------------
    # Plot
    # ----------------

    # Create stacked area chart
    fig = make_subplots(
        rows=1 if facet_row is None else len(da[facet_row]),
        cols=1 if facet_col is None else len(da[facet_col]),
        shared_xaxes="all",
        shared_yaxes=True,
        row_titles=None if facet_row is None else s[facet_row].values.astype("str").tolist(),
        column_titles=None if facet_col is None else s[facet_col].values.astype("str").tolist(),
        y_title="Energy balance (MWh)",
        x_title="Hours (h)",
    )

    add_to_legend = xr.DataArray(True, coords=[da.category])

    def plot_bar_chart(
        fig_,
        da0,
        row_var_=None,
        col_var_=None,
        row_=None,
        col_=None,
        showlegend_=showlegend,
        add_to_legend_=None,
    ):
        for category_ in da0.category.values:
            da_ = da0.sel(category=category_)
            da_ = da_ if row_var_ is None else da_.sel({facet_row: row_var_})
            da_ = da_ if col_var_ is None else da_.sel({facet_col: col_var_})
            da_ = da_.where(abs(da_) > threshold)
            if add_to_legend_ is not None and showlegend_:
                showlegend_ = bool(add_to_legend_.loc[dict(category=category_)])
                add_to_legend_.loc[dict(category=category_)] = False
            if abs(da_).max() > threshold:
                fig_.add_trace(
                    go.Bar(
                        x=x_axis,
                        y=da_,
                        marker=dict(color=color_map[category_], line=dict(width=0)),
                        name=str(category_),
                        showlegend=showlegend_,
                    ),
                    row=1 if row_ is None else row_ + 1,
                    col=1 if col_ is None else col_ + 1,
                )
        return fig_

    for row in [None] if facet_row is None else range(len(da[facet_row])):
        row_var = None if row is None else s[facet_row].values[row]
        for col in [None] if facet_col is None else range(len(da[facet_col])):
            col_var = None if col is None else s[facet_col].values[col]

            fig = plot_bar_chart(
                fig_=fig,
                da0=da,
                row_var_=row_var,
                col_var_=col_var,
                row_=row,
                col_=col,
                add_to_legend_=add_to_legend,
                showlegend_=showlegend,
            )

            if row is not None or col is not None:
                detailed_fig = go.Figure()

                detailed_fig = plot_bar_chart(
                    fig_=detailed_fig,
                    da0=da,
                    row_var_=row_var,
                    col_var_=col_var,
                    showlegend_=True,
                )

                detailed_fig.update_layout(
                    title=f"Hourly energy balance for {row_var} in {col_var}",
                    xaxis_title="Hour (h)",
                    yaxis_title="Energy balance (MWh)",
                    barmode="relative",
                    bargap=0,
                )

                folder = f"{plot_folder}/{plot_name}"
                if not os.path.exists(folder):
                    os.makedirs(folder)

                detailed_fig.write_html(f"{folder}/{col_var}_{row_var}.html")
    fig.update_layout(title="Hourly energy balance", barmode="relative", bargap=0)

    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)
    fig.write_html(
        f"{plot_folder}/{plot_name}.html",
        config={"responsive": False},
    )
    return fig


def plot_stock_level(
    model_parameters,
    model_solution,
    area,
    plot_folder,
    plot_name="stock_level",
    threshold=1e-6,
):
    s = model_solution
    p = model_parameters

    # ----------------
    # Data formatting
    # ----------------

    if not ("storage" in p.keys() and p.storage):
        Warning("No storage in simulation. No storage level graph generated.")
        return

    da = s.operation_storage_level.sel(area=area, drop=True)
    selection = da.max(dim=[dim for dim in da.dims if dim != "storage_tech"]) > threshold
    da = da.sel(storage_tech=da.storage_tech[selection]).sum("year_inv")

    # ----------------
    # Plot
    # ----------------

    fig = make_subplots(
        rows=len(da.storage_tech),
        cols=len(da.year_op),
        shared_xaxes=True,
        shared_yaxes=False,
        row_titles=da.storage_tech.values.tolist(),
        column_titles=da.year_op.values.astype("str").tolist(),
        y_title="Storage level (MWh)",
        x_title="Hours (h)",
    )

    for row in range(len(da.storage_tech)):
        storage_tech = da.storage_tech.values[row]

        for col in range(len(da.year_op)):
            year_op = da.year_op.values[col]

            x_axis = array_to_datetime(da.hour.values - 1, year_op)

            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=da.sel(storage_tech=storage_tech, year_op=year_op),
                    mode="lines",
                    name=storage_tech,
                    showlegend=True,
                ),
                row=row + 1,
                col=col + 1,
            )

    fig.update_layout(title="Hourly storage level")

    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)
    fig.write_html(f"{plot_folder}/{plot_name}.html")
    return fig


def plot_capacities(
    model_parameters,
    model_solution,
    area,
    plot_folder,
    plot_name="installed capacities",
    threshold=1e-6,
):
    # TODO: add year inv, transport management
    s = model_solution
    p = model_parameters

    # ----------------
    # Data formatting
    # ----------------

    ds_0 = s[[name for name in s.data_vars if "operation" in name and "capacity" in name]].sum(
        "year_inv"
    )

    ds_0 = ds_0.sel(area=area, drop=True)

    if model_parameters.transport:
        ds_0 = ds_0.sel(area_to=area, drop=True).sum("area_from")

    l_ds = []

    for variable in ds_0:
        ds = ds_0[variable]

        coord = [coord for coord in ds.coords if "tech" in coord][0]

        if threshold > 0:
            selection = ds.max(dim=[dim for dim in ds.dims if dim != coord]) > threshold
            ds = ds.sel({coord: selection})

        capacity_type = "power"
        if "energy" in variable:
            capacity_type = "energy"

        ds = ds.to_dataset(name=capacity_type)

        ds = ds.assign(category=xr.DataArray(coord.split("_tech")[0], coords=[ds[coord]]))

        ds = ds.rename({coord: "tech"})

        l_ds.append(ds)

    ds = xr.merge(l_ds)

    ds = ds.merge(get_main_resource(p), join="inner")

    resources = p.resource.sel(
        resource=p.resource.isin(ds.groupby("resource").sum("tech").resource)
    )

    demand = p.demand.max(dim=[dim for dim in p.demand.dims if dim not in ["year_op", "resource"]])

    # ----------------
    # Plot
    # ----------------

    category_colors = {
        "conversion": "blue",
        "storage": "red",
        "transport": "green"
        # Add more categories if needed
    }

    # DataArray index by (resource, year_op) True if storage installed for each tuple
    boolean_has_storage = (
        resources.where(np.logical_and(ds.energy > 0, ds.resource == resources))
        .notnull()
        .sum("tech")
    )

    row_titles = p.year_op.values.astype("str").tolist()
    column_titles = resources.values.astype("str").tolist()

    storage_legend = True
    show_legend_category = {"conversion": True, "storage": True, "transport": True}

    fig = make_subplots(
        rows=len(p.year_op),
        cols=len(resources),
        shared_xaxes=True,
        shared_yaxes="all",
        row_titles=row_titles,
        column_titles=column_titles,
        specs=[
            [
                {
                    "secondary_y": boolean_has_storage.sel(
                        year_op=year_op, resource=resource
                    ).to_numpy()
                }
                for resource in resources
            ]
            for year_op in p.year_op
        ],
        # x_title="Hours (h)",
    )

    for row in range(len(p.year_op)):
        year_op = p.year_op.values[row]

        for col in range(len(resources)):
            resource = resources.values[col]

            ds_plot = ds.sel(year_op=year_op, tech=ds.resource == resource)
            df_plot = ds_plot.to_dataframe().reset_index().sort_values(by=["category", "tech"])

            x_axis = df_plot[["category", "tech"]].sort_values(by=["category", "tech"]).to_numpy().T

            for category in df_plot["category"].unique():
                fig.add_trace(
                    go.Bar(
                        x=x_axis,
                        y=df_plot.where(df_plot["category"] == category, np.nan)["power"],
                        name=f"{category} power [MW]",
                        showlegend=show_legend_category[category],
                        marker_color=category_colors[category],
                    ),
                    secondary_y=False,
                    row=row + 1,
                    col=col + 1,
                )

                show_legend_category[category] = False

            if boolean_has_storage.sel(resource=resource, year_op=year_op):
                fig.add_trace(
                    go.Scatter(
                        x=x_axis,
                        y=df_plot["energy"],
                        name="storage energy [MWh]",
                        mode="markers",
                        marker=dict(
                            size=14,
                            color="purple",
                            symbol="diamond",
                        ),
                        showlegend=storage_legend,
                    ),
                    secondary_y=True,
                    row=row + 1,
                    col=col + 1,
                )

                storage_legend = False

                fig.update_yaxes(
                    secondary_y=True,
                    row=row + 1,
                    col=col + 1,
                    color="purple",
                    showgrid=False,
                    ticks="outside",
                    tickwidth=2,
                    tickcolor="purple",
                    ticklen=8,
                    range=[0, df_plot["energy"].max() * 1.2],
                )

            fig.add_hline(
                y=demand.sel(resource=resource, year_op=year_op).to_numpy(),
                line_width=2,
                line_dash="dash",
                secondary_y=False,
                showlegend=col == 0 and row == 0,
                name="max annual exogenous demand",
                row=row + 1,
                col=col + 1,
            )

        fig.update_yaxes(
            title="Installed power capacities [MW]",
            secondary_y=False,
            col=1,
            color="black",
            showgrid=True,
            ticks="outside",
            tickwidth=2,
            tickcolor="black",
            ticklen=8,
            # range=[0, 10],
        )
        fig.update_yaxes(
            title="Installed energy capacities [MWh]",
            secondary_y=True,
            col=len(resources),
        )

    fig.update_layout(
        title="Installed capacities",
        barmode="stack",
    )

    fig.for_each_annotation(lambda a: a.update(x=-0.07) if a.text in row_titles else ())

    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)
    fig.write_html(f"{plot_folder}/{plot_name}.html")
    return fig


def example_wedges():
    data = dict(
        techno=["nuke", "gas", "pv", "onshore"],
        label=["Nuclear", "Gas Power Plant", "Solar PV", "Wind Onshore"],
        installed_capacity=[45, 20, 20, 15],
        dispatch_power=[30, 10, 15, 10],
        color=["darkblue", "grey", "gold", "lightblue"],
    )
    df = pd.DataFrame(data).set_index("techno")

    df["installed_capacity_ratio"] = df["installed_capacity"] / df["installed_capacity"].sum()
    df["power_rate"] = df["dispatch_power"] / df["installed_capacity"]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

    theta1 = 280  # init, in deg
    sep = 2  # in deg

    data_portion = 360 - len(df.index) * sep

    for i, techno in enumerate(df.index):
        theta2 = theta1 + data_portion * df.loc[techno, "installed_capacity_ratio"]

        wedge_capa = patches.Wedge(
            center=(0, 0),
            r=1.0,
            theta1=theta1,
            theta2=theta2,
            width=0.3,
            edgecolor=df.loc[techno, "color"],
            facecolor="none",
            linewidth=2,
        )
        ax.add_patch(wedge_capa)

        wedge_power = patches.Wedge(
            center=(0, 0),
            r=0.95,
            theta1=theta2 - (theta2 - theta1) * df.loc[techno, "power_rate"],
            theta2=theta2,
            width=0.2,
            edgecolor="none",
            facecolor=df.loc[techno, "color"],
            linewidth=2,
        )
        ax.add_patch(wedge_power)

        theta1 = theta2 + sep
        theta2 = theta2 - 360 * (theta2 > 360)

    ax.axis("off")

    plt.show()
    return
