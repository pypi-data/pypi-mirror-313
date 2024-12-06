import pathlib

import pandas as pd
import yaml

from s2v.client.viz.jaal import Jaal
from s2v.client.viz.yaml_model_parser import YAMLModelParser

DEFAULT_VIZ_OPTS = {
    "height": "800px",
    "interaction": {
        "hover": True,  # Highlight node and its edges on hover
    },
    "physics": {"stabilization": {"iterations": 300}, "barnesHut": {"gravitationalConstant": -3000}},
    "layout": {"improvedLayout": True},
    "edges": {
        "font": {
            "color": "#ff5353",
            "size": 8,
        },
    },
}


def visualize(input_dir: pathlib.Path) -> None:
    parser = YAMLModelParser()

    for file in input_dir.rglob("*.yaml"):
        with file.open() as f:
            data = yaml.safe_load(f)
            parser.parse_entity(data)

    node_df = pd.DataFrame(parser.nodes)
    node_df = node_df.drop_duplicates(subset=["id"])

    edge_df = pd.DataFrame(parser.edges)
    # Group duplicates
    edge_df = (
        edge_df.groupby(["from", "to"])
        .agg(count=("from", "size"), title=("title", lambda titles: ", ".join(titles)))
        .reset_index()
    )

    # Initialize Jaal with the data and plot
    jaal = Jaal(edge_df=edge_df, node_df=node_df)
    jaal.plot(vis_opts=DEFAULT_VIZ_OPTS, port=8050)
