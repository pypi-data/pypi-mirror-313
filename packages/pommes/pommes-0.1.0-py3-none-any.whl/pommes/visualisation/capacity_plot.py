import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from pommes.io.calculate_summaries import generate_summary_dataframes_from_results


def plot_capacities(
    solution_path,
    tech_list,
    plot_choice,
    areas=None,
    years=None,
    rename=False,
    rename_dict={},
    title="Production capacities",
    save=True,
    save_name="capacities",
    color_dict=None,
):
    """
    Plot the production capacities of each technology selected. It is better te select technologies from the same type (ex: conversion)

    Parameters
    ----------
    solution_path : str
    tech_list : list of strings
    plot_choice : str (to choose between 'area' and 'year'. If 'year' is selected, only one area can be chosen and the other way around)
    areas : list of string (if None, all the areas are considered)
    years : list of ints (if None, all the years are considered)
    rename : bool, optional
    rename_dict : dict, optional (if you want to rename technologies)
    title : string, optional
    save : bool, optional (if you want to save the figure)
    save_name : str, optional
    color_dict : dict, optional (to personalise the graph colors. The structure of the dictionary should be key=technologie (non renamed) and value=color)


    Returns
    -------
    Plot the figure and save the plot if option is selected

    Exemple:
    >>> plot_capacities('solution_path',['atr','electrolysis','smr'],'area',years=[2050],title='Hydrogen production capacities')
    """

    if plot_choice not in ["area", "year"]:
        raise ValueError("you have to select either 'area' or 'year'.")

    solution = xr.open_dataset(solution_path + "solution.nc")
    parameters = xr.open_dataset(solution_path + "input.nc")
    summary = generate_summary_dataframes_from_results(solution, parameters)
    df_capa = summary["Production capacity - MW"]

    if len(tech_list) == 0:
        raise ValueError("no technologies selected. Select at least one technology.")
    if years == None:
        years = (
            df_capa.loc[(slice(None), slice(None), tech_list, slice(None))]
            .index.get_level_values("year_op")
            .unique()
            .to_list()
        )
    if areas == None:
        areas = (
            df_capa.loc[(slice(None), slice(None), tech_list, slice(None))]
            .index.get_level_values("area")
            .unique()
            .to_list()
        )
    if plot_choice == "area":
        not_choice = "year"
        if len(years) > 1:
            raise ValueError("if you select 'area' for plot choice, you can only choose one year.")
    else:
        not_choice = "area"
        if len(areas) > 1:
            raise ValueError("if you select 'year' for plot choice, you can only choose one area.")
    index_dic = {"area": "area", "year": "year_op"}
    label_dic = {"area": areas, "year": years}

    type = (
        df_capa.loc[(slice(None), areas[0], tech_list, years[0])]
        .index.get_level_values("type")
        .unique()
        .to_list()
    )
    if len(type) > 1:
        print("Warning, you selected different types of technologies")

    df_selected = df_capa.loc[(type, areas, tech_list, years)].reset_index(
        ["type", index_dic[not_choice]], drop=True
    )
    df_selected = (
        df_selected.reset_index()
        .pivot(columns="tech", values="power_capacity", index=index_dic[plot_choice])
        .rename(columns=rename_dict)
        .fillna(0)
    )
    if rename == True:
        tech_list_renamed = [rename_dict[tech] for tech in tech_list]
    else:
        tech_list_renamed = tech_list

    if color_dict == None:
        col = plt.cm.tab10
        color_dict_renamed = {}
        for k, tech in enumerate(tech_list_renamed):
            color_dict_renamed[tech] = col(k % 10)
    else:
        if rename == True:
            color_dict_renamed = {}
            for key in color_dict:
                color_dict_renamed[rename_dict[key]] = color_dict[key]
        else:
            color_dict_renamed = color_dict

    fig, ax = plt.subplots()
    width = 0.40
    labels = label_dic[plot_choice]
    x = np.arange(len(labels))

    l = []
    l_bottom = np.zeros(len(labels))
    for n, tech in enumerate(tech_list_renamed):
        l.append([val / 1000 for val in df_selected[tech].to_list()])
        ax.bar(
            x,
            l[n],
            width,
            bottom=l_bottom,
            label=tech_list_renamed[n],
            color=color_dict_renamed[tech],
            zorder=2,
        )
        l_bottom = [i + j for i, j in zip(l_bottom, l[n])]

    ax.grid(axis="y", alpha=0.5, zorder=1)
    ax.set_ylim([0, max(l_bottom) * 1.1])
    ax.set_ylabel("Installed capacity (GW)")
    ax.set_title(title)
    plt.xticks(x, labels, rotation=30)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + 0.05, box.width * 0.71, box.height * 0.95])
    handles, labels = ax.get_legend_handles_labels()
    order = sorted(np.arange(n + 1), reverse=True)
    ax.legend(
        [handles[idx] for idx in order],
        [labels[idx] for idx in order],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )
    if save == True:
        plt.savefig(solution_path + save_name + ".png")
    plt.show()
    return
