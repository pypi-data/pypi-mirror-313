# ruff: noqa: E722, S110
"""
Author: Mohit Mayank

Layout code for the application
"""

# Import
# ---------
import base64
import pathlib

import dash_bootstrap_components as dbc
import pandas as pd
import visdcc
from dash import html

# Constants
# --------------
# default node and edge size
DEFAULT_NODE_SIZE = 20
DEFAULT_EDGE_SIZE = 1
DEFAULT_BORDER_SIZE = 1

# default node and egde color
# DEFAULT_NODE_COLOR = '#97C2FC'
# DEFAULT_EDGE_COLOR = '#FFFFFF'

# Taken from https://stackoverflow.com/questions/470690/how-to-automatically-generate-n-distinct-colors
KELLY_COLORS_HEX = [
    "#FFB300",  # Vivid Yellow
    "#803E75",  # Strong Purple
    "#FF6800",  # Vivid Orange
    "#A6BDD7",  # Very Light Blue
    "#C10020",  # Vivid Red
    "#CEA262",  # Grayish Yellow
    "#817066",  # Medium Gray
    # The following don't work well for people with defective color vision
    "#007D34",  # Vivid Green
    "#F6768E",  # Strong Purplish Pink
    "#00538A",  # Strong Blue
    "#FF7A5C",  # Strong Yellowish Pink
    "#53377A",  # Strong Violet
    "#FF8E00",  # Vivid Orange Yellow
    "#B32851",  # Strong Purplish Red
    "#F4C800",  # Vivid Greenish Yellow
    "#7F180D",  # Strong Reddish Brown
    "#93AA00",  # Vivid Yellowish Green
    "#593315",  # Deep Yellowish Brown
    "#F13A13",  # Vivid Reddish Orange
    "#232C16",  # Dark Olive Green
]

DEFAULT_OPTIONS = {
    "height": "100%",
    "width": "100%",
    "interaction": {"hover": True},
    "physics": {"stabilization": {"iterations": 300}},
    "autoResize": True,
}


# Code
# ---------
def get_options(directed, opts_args):
    opts = DEFAULT_OPTIONS.copy()
    opts["edges"] = {"arrows": {"to": directed}}
    if opts_args is not None:
        opts.update(opts_args)
    return opts


def get_distinct_colors(n):
    """Return distict colors, currently atmost 20

    Parameters
    -----------
    n: int
        the distinct colors required
    """
    if n <= 20:  # noqa: PLR2004
        return KELLY_COLORS_HEX[:n]


def create_card(id, value, description):
    """Creates card for high level stats

    Parameters
    ---------------
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(id=id, children=value, className="card-title"),
                html.P(children=description),
            ]
        )
    )


def create_color_legend(text, color):
    """Individual row for the color legend"""
    return create_row(
        [
            html.Div(style={"width": "10px", "height": "10px", "background-color": color}),
            html.Div(text, style={"padding-left": "10px"}),
        ]
    )


_FLEX_ROW_STYLE = {"display": "flex", "flex-direction": "row", "justify-content": "center", "align-items": "center"}


def create_row(children, style=_FLEX_ROW_STYLE):
    return dbc.Row(children, style=style, className="column flex-display")


def get_select_form_layout(id, options, label, description):
    """Creates a select (dropdown) form with provides details

    Parameters
    -----------
    id: str
        id of the form
    options: list
        options to show
    label: str
        label of the select dropdown bar
    description: str
        long text detail of the setting
    """
    return dbc.Form(
        [
            dbc.InputGroup(
                [
                    dbc.InputGroupText(label),
                    dbc.Select(id=id, options=options),
                ]
            ),
            dbc.FormText(description, color="secondary"),
        ]
    )


search_form = dbc.Form(
    [
        dbc.InputGroup(
            [
                dbc.Input(type="search", id="search_graph", placeholder="Search node in graph..."),
                dbc.Button("Search", id="search_button", color="secondary"),
            ]
        ),
        dbc.FormText(
            "Show the node you are looking for",
            color="secondary",
        ),
        html.Hr(className="my-2"),
    ],
    style={
        "width": "96%",
        "margin-left": "auto",
        "margin-right": "auto",
        "display": "block",
    },
)

find_connection_form = dbc.Form(
    [
        dbc.Input(type="search", id="search_from_graph", placeholder="Connection from node..."),
        dbc.Input(type="search", id="search_to_graph", placeholder="Connection to node..."),
        dbc.FormText(
            "Search connections between two nodes",
            color="secondary",
        ),
        dbc.Row(
            [
                dbc.Col(
                    get_select_form_layout(
                        id="search_distance",
                        options=[
                            {"label": "2", "value": 2},
                            {"label": "3", "value": 3},
                            {"label": "4", "value": 4},
                            {"label": "5", "value": 5},
                            {"label": "6", "value": 6},
                            {"label": "Not specified", "value": "Any"},
                        ],
                        label="Distance",
                        description="Set maximum path length",
                    ),
                ),
                dbc.Col(
                    dbc.Button(
                        "Search",
                        id="find_connection_button",
                        color="secondary",
                        size="sm",
                        style={
                            "width": "100%",
                            "height": "62%",
                            "margin-bottom": "auto",
                            "margin-left": "auto",
                            "margin-right": "auto",
                            "display": "block",
                        },
                    ),
                    width="auto",
                ),
            ],
            style={
                "margin-top": "10px",
            },
        ),
    ],
    style={
        "margin-top": "10px",
        "width": "96%",
        "margin-left": "auto",
        "margin-right": "auto",
        "display": "block",
    },
)

nodes_with_no_edges_form = dbc.Form(
    [
        html.Hr(className="my-2"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormText(
                        "Show nodes with no edges",
                        color="secondary",
                        style={
                            "font-size": "1rem",
                        },
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Checkbox(
                        id="nodes_with_no_edges_checkbox",
                        value=False,
                        className="float-right",
                        style={
                            "transform": "scale(1.5)",
                            "margin-top": "0.25em",
                            "vertical-align": "middle",
                        },
                    ),
                    width="auto",
                ),
            ],
            align="center",
        ),
        html.Hr(className="my-2"),
    ],
    style={
        "margin-top": "10px",
        "width": "96%",
        "margin-left": "auto",
        "margin-right": "auto",
        "display": "block",
    },
)

filter_node_form = dbc.Form(
    [
        dbc.Textarea(id="filter_nodes", placeholder="Enter filter node query here..."),
        dbc.FormText(
            html.P(
                [
                    "Filter on nodes properties by using ",
                    html.A(
                        "Pandas Query syntax",
                        href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html",
                    ),
                ]
            ),
            color="secondary",
        ),
    ]
)

filter_edge_form = dbc.Form(
    [
        dbc.Textarea(id="filter_edges", placeholder="Enter filter edge query here..."),
        dbc.FormText(
            html.P(
                [
                    "Filter on edges properties by using ",
                    html.A(
                        "Pandas Query syntax",
                        href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html",
                    ),
                ]
            ),
            color="secondary",
        ),
    ]
)


def get_categorical_features(df_, unique_limit=20, blacklist_features=None):
    """Identify categorical features for edge or node data and return their names
    Additional logics: (1) cardinality should be within `unique_limit`, (2) remove blacklist_features
    """
    # identify the rel cols + None
    if blacklist_features is None:
        blacklist_features = ["shape", "label", "id"]
    cat_features = [
        "None",
        *df_.columns[(df_.dtypes == "object") & (df_.apply(pd.Series.nunique) <= unique_limit)].tolist(),
    ]
    # remove irrelevant cols
    try:
        for col in blacklist_features:
            cat_features.remove(col)
    except:
        pass
    # return
    return cat_features


def get_numerical_features(df_):
    """Identify numerical features for edge or node data and return their names"""
    # supported numerical cols
    numerics = ["int16", "int32", "int64", "float16", "float32", "float64"]
    # identify numerical features
    numeric_features = ["None", *df_.select_dtypes(include=numerics).columns.tolist()]
    # remove blacklist cols (for nodes)
    try:
        numeric_features.remove("size")
        numeric_features.remove("node_image_url")
        numeric_features.remove("image")
    except:
        pass
    # return
    return numeric_features


def get_app_layout(graph_data, color_legends=None, directed=False, vis_opts=None):
    """Create and return the layout of the app

    Parameters
    --------------
    graph_data: dict{nodes, edges}
        network data in format of visdcc
    """
    # Get numerical features of nodes and edges
    if color_legends is None:
        color_legends = []
    num_node_features = get_numerical_features(pd.DataFrame(graph_data["nodes"]))
    num_edge_features = get_numerical_features(pd.DataFrame(graph_data["edges"]))
    # Create and return the layout
    # Resolve path
    this_file = pathlib.Path(__file__)
    this_dir = this_file.parent
    image_filename = this_dir / "assets" / "logo.png"
    with image_filename.open("rb") as f:
        encoded_image = base64.b64encode(f.read())
    return html.Div(
        [
            # floating logo
            create_row(
                html.Div(
                    html.Img(src=f"data:image/png;base64,{encoded_image.decode()}", style={"width": "60px"}),
                    style={
                        "position": "fixed",
                        "top": "10px",
                        "left": "90%",
                        "z-index": "1000",
                        "background-color": "#e5e5e5",
                        "padding": "10px",
                    },
                ),
            ),
            # settings panel
            html.Div(
                dbc.Form(
                    [
                        # ---- search section ----
                        create_row(
                            [
                                dbc.Button(
                                    "Clear Search",
                                    id="clear_search_button",
                                    outline=True,
                                    color="secondary",
                                    size="sm",
                                    style={
                                        "width": "auto",
                                        "marginTop": "10px",
                                    },
                                )
                            ],
                        ),
                        html.Hr(className="my-2"),
                        search_form,
                        # ---- find path section ----
                        find_connection_form,
                        # ---- no edges section ----
                        nodes_with_no_edges_form,
                        # ---- size section ----
                        create_row(
                            [
                                dbc.Button(
                                    "Reset Sizing",
                                    id="clear_size_button",
                                    outline=True,
                                    color="secondary",
                                    size="sm",
                                    style={"width": "auto"},
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                get_select_form_layout(
                                    id="size_nodes",
                                    options=[{"label": opt, "value": opt} for opt in num_node_features],
                                    label="Size nodes by",
                                    description="Size nodes by a numerical node property",
                                ),
                                get_select_form_layout(
                                    id="size_edges",
                                    options=[{"label": opt, "value": opt} for opt in num_edge_features],
                                    label="Size edges by",
                                    description="Size edges by a numerical edge property",
                                ),
                            ],
                            style={
                                "width": "96%",
                                "margin-left": "auto",
                                "margin-right": "auto",
                                "margin-bottom": "10px",
                                "margin-top": "10px",
                            },
                        ),
                    ],
                    style={
                        "width": "300px",
                        "height": "500",
                        "position": "fixed",
                        "top": "30px",
                        "left": "30px",
                        "z-index": "800",
                        "background": "#e5e5e5",
                    },
                ),
            ),
            html.Div(
                visdcc.Network(  # type: ignore[attr-defined]
                    id="graph",
                    data=graph_data,
                    options=get_options(directed, vis_opts),
                    style={
                        "width": "100%",
                        "height": "100vh",
                    },
                ),
            ),
        ],
    )
