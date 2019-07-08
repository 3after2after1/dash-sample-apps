# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import random

from dash.dependencies import Input, Output
from utils import *

app = dash.Dash(__name__)
server = app.server

virus_name = "measles"
species = ["Avian", "Ebola", "Lassa", "Measles", "Mumps", "Zika"]
tree_fig = {}
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"


tree_file, metadata_file, metadata_file_stat = create_paths_file(
    virus_name, level1="", level2="", level3=""
)
# To know the minimum and the maximum values of date for slicer
df_stat_metadata = pd.read_csv(metadata_file_stat)
min_date, max_date = min_max_date(df_stat_metadata)
# create the dictionary of slider
marks_data = slicer(min_date, max_date)
min_max_date_value = [min_date, max_date]

fig = create_tree(virus_name, tree_file, metadata_file, "Country")
tree_fig[tree_file] = fig

fig_map_bubble = create_map_bubble_year(
    virus_name, metadata_file_stat, 2, min_date, max_date
)
fig_curve_line = create_curve_line(df_stat_metadata, virus_name, min_date, max_date)


######################################### MAIN APP #########################################
app.layout = html.Div(
    [
        # Banner display
        html.Div(
            className="header-title",
            children=[
                html.H2(
                    id="title",
                    children="Phylogeny trees and global spread of 6 viruses",
                ),
                html.Div(
                    id="learn_more",
                    children=[
                        html.Img(
                            className="logo",
                            src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png",
                        ),
                        html.Button(className="btn", children=["Learn      More"]),
                    ],
                ),
            ],
        ),
        html.Div(
            id="grid",
            children=[
                html.Div(
                    id="controls",
                    className="row div-row div-card",
                    children=[
                        html.Div(
                            id="dataset-picker",
                            children=[
                                html.Div(
                                    className="six columns",
                                    children=[
                                        html.H6(children="Dataset"),
                                        dcc.Dropdown(
                                            id="d_virus-name",
                                            options=[
                                                {"label": species[i], "value": species[i]}
                                                for i in range(len(species))
                                            ],
                                            value="Measles",
                                        ),
                                        html.Div(id="output-container"),
                                    ],
                                ),
                                # Strain dropdown picker
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="four columns",
                                            children=[
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            id="controls-container_mumps",
                                                            children=[
                                                                dcc.Dropdown(
                                                                    id="d_mumps",
                                                                    options=[
                                                                        {"label": i, "value": i}
                                                                        for i in [
                                                                            "global",
                                                                            "na",
                                                                        ]
                                                                    ],
                                                                    value="global",
                                                                )
                                                            ],
                                                        ),
                                                        html.Div(
                                                            id="controls-container_dengue",
                                                            children=[
                                                                dcc.Dropdown(
                                                                    id="d_dengue",
                                                                    options=[
                                                                        {"label": i, "value": i}
                                                                        for i in [
                                                                            "all",
                                                                            "denv1",
                                                                            "denv2",
                                                                            "denv3",
                                                                            "denv4",
                                                                        ]
                                                                    ],
                                                                    value="all",
                                                                )
                                                            ],
                                                        ),
                                                        html.Div(
                                                            id="controls-container_lassa",
                                                            children=[
                                                                dcc.Dropdown(
                                                                    id="d_lassa",
                                                                    options=[
                                                                        {"label": i, "value": i}
                                                                        for i in ["s", "l"]
                                                                    ],
                                                                    value="s",
                                                                )
                                                            ],
                                                        ),
                                                        html.Div(
                                                            id="controls-container_avian",
                                                            children=[
                                                                dcc.Dropdown(
                                                                    id="d_avian_opt1",
                                                                    options=[
                                                                        {"label": i, "value": i}
                                                                        for i in ["h7n9"]
                                                                    ],
                                                                    value="h7n9",
                                                                ),
                                                                dcc.Dropdown(
                                                                    id="d_avian_opt2",
                                                                    options=[
                                                                        {"label": i, "value": i}
                                                                        for i in [
                                                                            "ha",
                                                                            "mp",
                                                                            "na",
                                                                            "ns",
                                                                            "np",
                                                                            "pa",
                                                                            "pb2",
                                                                            "pb1",
                                                                        ]
                                                                    ],
                                                                    value="ha",
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            id="controls-container_flu",
                                                            children=[
                                                                dcc.Dropdown(
                                                                    id="d_flu_opt1",
                                                                    options=[
                                                                        {"label": i, "value": i}
                                                                        for i in [
                                                                            "h3n2",
                                                                            "h1n1pdm",
                                                                            "vic",
                                                                            "yam",
                                                                        ]
                                                                    ],
                                                                    value="h3n2",
                                                                ),
                                                                dcc.Dropdown(
                                                                    id="d_flu_opt2",
                                                                    options=[
                                                                        {"label": i, "value": i}
                                                                        for i in ["ha", "na"]
                                                                    ],
                                                                    value="ha",
                                                                ),
                                                                dcc.Dropdown(
                                                                    id="d_flu_opt3",
                                                                    options=[
                                                                        {"label": i, "value": i}
                                                                        for i in [
                                                                            "2y",
                                                                            "3y",
                                                                            "6y",
                                                                            "12y",
                                                                        ]
                                                                    ],
                                                                    value="3y",
                                                                ),
                                                            ],
                                                        ),
                                                    ]
                                                )
                                            ],
                                        )
                                    ],
                                ),
                            ]
                        ),
                        
                        html.Div(
                            className="six columns",
                            children=[
                                html.H6(children="Data Range"),
                                html.Div(
                                    id="id-slicer",
                                    children=[
                                        dcc.RangeSlider(
                                            id="id-year",
                                            min=min_date,
                                            max=max_date,
                                            step=1,
                                            marks=marks_data,
                                            value=min_max_date_value,
                                            vertical=True,
                                        )
                                    ],
                                ),
                            ],
                        ),
                        
                    ],
                ),
                
                dcc.Graph(
                    id="curve-line-graph", 
                    className="div-card",
                    figure=fig_curve_line,
                ),

                dcc.Graph(
                    id="phylogeny-graph",
                    className="div-card",
                ),

                dcc.Graph(
                    id="map-graph", 
                    className="div-card",
                    figure=fig_map_bubble,
                ),

                dcc.Graph(
                    id="histo-graph",
                    className="div-card",
                ),
            ],
        ),
    ]
)


######################################### UPDATING FIGURES #########################################
@app.callback(Output("output-container", "children"), [Input("d_virus-name", "value")])
def _update_legend_gene(virus_name):
    return 'You have selected "{}" virus'.format(virus_name)


@app.callback(
    Output("controls-container_mumps", "style"), [Input("d_virus-name", "value")]
)
def _update_mumps_option(virus_name):
    if virus_name == "Mumps":
        return {"display": "block"}
    else:
        return {"display": "none"}


@app.callback(
    Output("controls-container_dengue", "style"), [Input("d_virus-name", "value")]
)
def _update_dengue_option(virus_name):
    if virus_name == "Dengue":
        return {"display": "block"}
    else:
        return {"display": "none"}


@app.callback(
    Output("controls-container_lassa", "style"), [Input("d_virus-name", "value")]
)
def _update_lassa_option(virus_name):
    if virus_name == "Lassa":
        return {"display": "block"}
    else:
        return {"display": "none"}


@app.callback(
    Output("controls-container_avian", "style"), [Input("d_virus-name", "value")]
)
def _update_avian_option(virus_name):
    if virus_name == "Avian":
        return {"display": "block"}
    else:
        return {"display": "none"}


@app.callback(
    Output("controls-container_flu", "style"), [Input("d_virus-name", "value")]
)
def _update_flu_option(virus_name):
    if virus_name == "Flu":
        return {"display": "block"}
    else:
        return {"display": "none"}


@app.callback(
    Output("phylogeny-graph", "figure"),
    [
        Input("d_virus-name", "value"),
        Input("d_mumps", "value"),
        Input("d_dengue", "value"),
        Input("d_lassa", "value"),
        Input("d_avian_opt1", "value"),
        Input("d_avian_opt2", "value"),
        Input("d_flu_opt1", "value"),
        Input("d_flu_opt2", "value"),
        Input("d_flu_opt3", "value"),
    ],
)
def _update_pĥylogentic_tree(
    virus_name,
    mumps,
    dengue,
    lassa,
    avian_opt1,
    avian_opt2,
    flu_opt1,
    flu_opt2,
    flu_opt3,
):
    virus_name = virus_name.lower()
    ord_by_elt = "Country"
    if virus_name == "ebola" or virus_name == "zika" or virus_name == "measles":
        data_virus_info = {
            "virus_name": virus_name,
            "level1": "",
            "level2": "",
            "level3": "",
        }
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1="", level2="", level3=""
        )
    elif virus_name == "mumps":
        data_virus_info = {
            "virus_name": virus_name,
            "level1": mumps,
            "level2": "",
            "level3": "",
        }
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=mumps, level2="", level3=""
        )
    elif virus_name == "dengue":
        data_virus_info = {
            "virus_name": virus_name,
            "level1": dengue,
            "level2": "",
            "level3": "",
        }
        tree_file_filtred, metadata_file_filtred, metadata_file_stat = create_paths_file(
            virus_name, level1=dengue, level2="", level3=""
        )
    elif virus_name == "lassa":
        data_virus_info = {
            "virus_name": virus_name,
            "level1": lassa,
            "level2": "",
            "level3": "",
        }
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=lassa, level2="", level3=""
        )
    elif virus_name == "avian":
        data_virus_info = {
            "virus_name": virus_name,
            "level1": avian_opt1,
            "level2": avian_opt2,
            "level3": "",
        }
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=avian_opt1, level2=avian_opt2, level3=""
        )
    elif virus_name == "flu":
        data_virus_info = {
            "virus_name": virus_name,
            "level1": flu_opt1,
            "level2": flu_opt2,
            "level3": flu_opt3,
        }
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=flu_opt1, level2=flu_opt2, level3=flu_opt3
        )

    if tree_file_filtred in tree_fig:
        fig = tree_fig[tree_file_filtred]
    else:
        if ord_by_elt == "Country" or ord_by_elt == "Division" or ord_by_elt == "Date":
            fig = create_tree(
                virus_name, tree_file_filtred, metadata_file_filtred, ord_by_elt
            )

        tree_fig[tree_file_filtred] = fig
    return fig


@app.callback(
    Output("map-graph", "figure"),
    [
        Input("d_virus-name", "value"),
        Input("d_mumps", "value"),
        Input("d_dengue", "value"),
        Input("d_lassa", "value"),
        Input("d_avian_opt1", "value"),
        Input("d_avian_opt2", "value"),
        Input("d_flu_opt1", "value"),
        Input("d_flu_opt2", "value"),
        Input("d_flu_opt3", "value"),
        Input("id-year", "value"),
    ],
)
def _update_map(
    virus_name,
    mumps,
    dengue,
    lassa,
    avian_opt1,
    avian_opt2,
    flu_opt1,
    flu_opt2,
    flu_opt3,
    id_year,
):
    virus_name = virus_name.lower()
    if virus_name == "ebola" or virus_name == "zika" or virus_name == "measles":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1="", level2="", level3=""
        )
    elif virus_name == "mumps":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=mumps, level2="", level3=""
        )
    elif virus_name == "dengue":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=dengue, level2="", level3=""
        )
    elif virus_name == "lassa":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=lassa, level2="", level3=""
        )
    elif virus_name == "avian":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=avian_opt1, level2=avian_opt2, level3=""
        )
    elif virus_name == "flu":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=flu_opt1, level2=flu_opt2, level3=flu_opt3
        )
    df = pd.read_csv(metadata_file_stat_filtred)

    min_date, max_date = id_year
    # To select only the data between min_date and max_date
    df = df[df["Year"] >= min_date]
    df = df[df["Year"] <= max_date]
    return create_map_bubble_year(
        virus_name, metadata_file_stat_filtred, 2, min_date, max_date
    )


@app.callback(
    Output("id-slicer", "children"),
    [
        Input("d_virus-name", "value"),
        Input("d_mumps", "value"),
        Input("d_dengue", "value"),
        Input("d_lassa", "value"),
        Input("d_avian_opt1", "value"),
        Input("d_avian_opt2", "value"),
        Input("d_flu_opt1", "value"),
        Input("d_flu_opt2", "value"),
        Input("d_flu_opt3", "value"),
    ],
)
def _update_slicer(
    virus_name,
    mumps,
    dengue,
    lassa,
    avian_opt1,
    avian_opt2,
    flu_opt1,
    flu_opt2,
    flu_opt3,
):
    virus_name = virus_name.lower()
    if virus_name == "ebola" or virus_name == "zika" or virus_name == "measles":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1="", level2="", level3=""
        )
    elif virus_name == "mumps":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=mumps, level2="", level3=""
        )
    elif virus_name == "dengue":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=dengue, level2="", level3=""
        )
    elif virus_name == "lassa":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=lassa, level2="", level3=""
        )
    elif virus_name == "avian":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=avian_opt1, level2=avian_opt2, level3=""
        )
    elif virus_name == "flu":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=flu_opt1, level2=flu_opt2, level3=flu_opt3
        )
    df = pd.read_csv(metadata_file_stat_filtred)
    min_date, max_date = min_max_date(df)
    # create the dictionary of slider
    marks_data = slicer(min_date, max_date)
    min_max_date_value = [min_date, max_date]

    # To select only the data between min_date and max_date
    df = df[df["Year"] >= min_date]
    df = df[df["Year"] <= max_date]
    return dcc.RangeSlider(
        id="id-year",
        min=min_date,
        max=max_date,
        step=1,
        marks=marks_data,
        value=min_max_date_value,
    )


@app.callback(
    Output("curve-line-graph", "figure"),
    [
        Input("d_virus-name", "value"),
        Input("d_mumps", "value"),
        Input("d_dengue", "value"),
        Input("d_lassa", "value"),
        Input("d_avian_opt1", "value"),
        Input("d_avian_opt2", "value"),
        Input("d_flu_opt1", "value"),
        Input("d_flu_opt2", "value"),
        Input("d_flu_opt3", "value"),
        Input("id-year", "value"),
    ],
)
def _update_curve(
    virus_name,
    mumps,
    dengue,
    lassa,
    avian_opt1,
    avian_opt2,
    flu_opt1,
    flu_opt2,
    flu_opt3,
    id_year,
):
    virus_name = virus_name.lower()
    if virus_name == "ebola" or virus_name == "zika" or virus_name == "measles":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1="", level2="", level3=""
        )
    elif virus_name == "mumps":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=mumps, level2="", level3=""
        )
    elif virus_name == "dengue":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=dengue, level2="", level3=""
        )
    elif virus_name == "lassa":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=lassa, level2="", level3=""
        )
    elif virus_name == "avian":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=avian_opt1, level2=avian_opt2, level3=""
        )
    elif virus_name == "flu":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=flu_opt1, level2=flu_opt2, level3=flu_opt3
        )
    df = pd.read_csv(metadata_file_stat_filtred)
    min_date, max_date = id_year

    # To select only the data between min_date and max_date
    df = df[df["Year"] >= min_date]
    df = df[df["Year"] <= max_date]

    return create_curve_line(df, virus_name, min_date, max_date)


@app.callback(
    Output("histo-graph", "figure"),
    [
        Input("d_virus-name", "value"),
        Input("d_mumps", "value"),
        Input("d_dengue", "value"),
        Input("d_lassa", "value"),
        Input("d_avian_opt1", "value"),
        Input("d_avian_opt2", "value"),
        Input("d_flu_opt1", "value"),
        Input("d_flu_opt2", "value"),
        Input("d_flu_opt3", "value"),
        Input("id-year", "value"),
    ],
)
def _update_histo(
    virus_name,
    mumps,
    dengue,
    lassa,
    avian_opt1,
    avian_opt2,
    flu_opt1,
    flu_opt2,
    flu_opt3,
    id_year,
):
    virus_name = virus_name.lower()
    if virus_name == "ebola" or virus_name == "zika" or virus_name == "measles":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1="", level2="", level3=""
        )
    elif virus_name == "mumps":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=mumps, level2="", level3=""
        )
    elif virus_name == "dengue":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=dengue, level2="", level3=""
        )
    elif virus_name == "lassa":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=lassa, level2="", level3=""
        )
    elif virus_name == "avian":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=avian_opt1, level2=avian_opt2, level3=""
        )
    elif virus_name == "flu":
        tree_file_filtred, metadata_file_filtred, metadata_file_stat_filtred = create_paths_file(
            virus_name, level1=flu_opt1, level2=flu_opt2, level3=flu_opt3
        )
    df = pd.read_csv(metadata_file_stat_filtred)
    min_date, max_date = id_year

    # To select only the data between min_date and max_date
    df = df[df["Year"] >= min_date]
    df = df[df["Year"] <= max_date]

    # Count the number of viruses by Country
    df_group_by_country = df.groupby(["Country"])["Value"].sum()
    # Translate groupby object in dataframe
    df_group_by_country = df_group_by_country.to_frame()
    # Rename the first column in Value
    df_group_by_country.columns = ["Value"]
    # Move the index values (i.e. Country column) in column and reset index
    df_group_by_country = df_group_by_country.reset_index()

    return {
        "data": [
            {
                "x": df_group_by_country["Country"],
                "y": df_group_by_country["Value"],
                "type": "bar",
            }
        ],
        "layout": {
            "autosize": True,
            "margin": "0px 0px 0px 0px",
            "title": "<br>Distribution of {} <br>Between {} and {}".format(
                virus_name.title(), min_date, max_date
            ),
        },
    }


######################################### CSS #########################################
external_css = ["https://fonts.googleapis.com/css?family=Lato"]

for css in external_css:
    app.css.append_css({"external_url": css})


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
